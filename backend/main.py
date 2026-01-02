import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Tuple, Optional
import time
import logging
from dataclasses import dataclass
import re
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrawlError(Exception):
    """Base exception for crawling errors"""
    pass

class ContentExtractionError(Exception):
    """Exception for content extraction errors"""
    pass

class EmbeddingError(Exception):
    """Exception for embedding generation errors"""
    pass

class StorageError(Exception):
    """Exception for storage errors"""
    pass

def retry_on_failure(max_retries=3, delay=1, backoff=2):
    """
    Decorator to retry a function on failure with exponential backoff.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay

            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries: {e}")
                        raise e

                    logger.warning(f"Function {func.__name__} failed (attempt {retries}/{max_retries}): {e}")
                    time.sleep(current_delay + random.uniform(0, 1))  # Add jitter
                    current_delay *= backoff

        return wrapper
    return decorator

@dataclass
class Chunk:
    id: str
    content: str
    url: str
    section: str
    heading: str
    word_count: int
    token_count: int
    source_position: int
    embedding: Optional[List[float]] = None

@retry_on_failure(max_retries=3, delay=1, backoff=2)
def get_all_urls(base_url: str) -> Tuple[List[str], Dict]:
    """
    Discover and return all accessible URLs from the Docusaurus website.

    Args:
        base_url (str): Base URL of the Docusaurus site

    Returns:
        Tuple[List[str], Dict]: List of URLs and metadata about the crawl
    """
    logger.info(f"Starting URL discovery from: {base_url}")

    start_time = time.time()
    urls = set()
    errors = []

    # First, try to get URLs from sitemap
    sitemap_url = urljoin(base_url, 'sitemap.xml')

    # Try the specific sitemap URL
    potential_sitemap_urls = [
        sitemap_url,
        'https://tayyaba10.github.io/humanoid_robotics_textbook/sitemap.xml'  # Specific to this project
    ]

    sitemap_found = False
    for potential_sitemap in potential_sitemap_urls:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(potential_sitemap, headers=headers, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')

                # Handle both regular sitemaps and sitemap indexes
                if soup.find('sitemapindex'):
                    # This is a sitemap index, get individual sitemaps
                    logger.info(f"Found sitemap index, processing individual sitemaps from: {potential_sitemap}")
                    for sitemap_loc in soup.find_all('loc'):
                        sitemap_loc_url = sitemap_loc.get_text().strip()
                        if sitemap_loc_url:
                            sitemap_response = requests.get(sitemap_loc_url, headers=headers, timeout=30)
                            if sitemap_response.status_code == 200:
                                sitemap_soup = BeautifulSoup(sitemap_response.content, 'xml')
                                for loc in sitemap_soup.find_all('loc'):
                                    url = loc.get_text().strip()
                                    if url and url.startswith(base_url):
                                        urls.add(url)
                                logger.info(f"Added URLs from sitemap: {sitemap_loc_url}")
                else:
                    # This is a regular sitemap
                    logger.info(f"Processing regular sitemap: {potential_sitemap}")
                    for loc in soup.find_all('loc'):
                        url = loc.get_text().strip()
                        if url and url.startswith(base_url):
                            urls.add(url)

                logger.info(f"Found {len(urls)} URLs from sitemap: {potential_sitemap}")
                sitemap_found = True
                break
            else:
                logger.warning(f"Sitemap {potential_sitemap} returned status code: {response.status_code}")
        except Exception as e:
            logger.warning(f"Error accessing sitemap {potential_sitemap}: {e}")
            continue

    # Even if sitemap was found, also do a basic crawl to ensure we don't miss any URLs
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(base_url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links on the main page
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)

            # Only add URLs from the same domain and that start with the base URL
            if (urlparse(full_url).netloc == urlparse(base_url).netloc and
                full_url.startswith(base_url) and
                not any(full_url.endswith(ext) for ext in ['.pdf', '.jpg', '.png', '.zip', '.exe'])):
                urls.add(full_url)
    except Exception as e:
        logger.warning(f"Warning during basic crawling: {e}")
        errors.append(str(e))

    # Remove any URLs that don't belong to the site
    filtered_urls = [url for url in urls if url.startswith(base_url)]

    crawl_time = time.time() - start_time

    metadata = {
        'total_urls': len(filtered_urls),
        'crawl_time': crawl_time,
        'errors': errors
    }

    logger.info(f"URL discovery completed. Found {len(filtered_urls)} URLs in {crawl_time:.2f}s")
    return filtered_urls, metadata

@retry_on_failure(max_retries=3, delay=1, backoff=2)
def extract_text_from_url(url: str) -> Tuple[str, Dict]:
    """
    Extract and clean text content from a specific URL.

    Args:
        url (str): URL to extract content from

    Returns:
        Tuple[str, Dict]: Cleaned content and metadata about the page
    """
    logger.info(f"Extracting content from: {url}")

    start_time = time.time()

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script, style, navigation, TOC, sidebar, header, footer, and other non-content elements
        for element in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
            element.decompose()

        # Remove TOC/"On this page" elements which are typically in elements with classes like "table-of-contents", "toc", "on-page", etc.
        for element in soup.find_all(['div', 'section'], class_=re.compile(r'.*\b(table-of-contents|toc|on-page|sidebar|navigation|menu|footer|header)\b.*', re.IGNORECASE)):
            element.decompose()

        # Extract content only from the <article> tag
        content_element = soup.find('article')

        # If no article tag found, return empty content (no fallback to main or body)
        if not content_element:
            content = ""
        else:
            for toc in content_element.select(
                '[class*="toc"], [class*="tableOfContents"], [class*="onThisPage"], nav'
            ):
                toc.decompose()
                
            # Extract text from the article element
            content = content_element.get_text(separator=' ', strip=True)

        # Clean up the text
        content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
        content = content.strip()

        # Extract metadata
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ""

        # Get description from meta tag
        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag.get('content', '') if description_tag else ""

        # Try to find the main heading (h1) for the page
        h1_element = soup.find('h1')
        heading = h1_element.get_text().strip() if h1_element else ""

        # If no h1, try h2
        if not heading:
            h2_element = soup.find('h2')
            heading = h2_element.get_text().strip() if h2_element else ""

        # Extract section from URL path (more specific to Docusaurus)
        path_parts = urlparse(url).path.strip('/').split('/')
        section = path_parts[0] if path_parts and path_parts[0] else "home"

        # If first part is common web directory name, use the second part
        if section in ['docs', 'blog', 'pages']:
            section = path_parts[1] if len(path_parts) > 1 else section

        # Calculate word count
        word_count = len(content.split())

        processing_time = time.time() - start_time

        metadata = {
            'title': title,
            'heading': heading,
            'section': section,
            'description': description,
            'word_count': word_count,
            'processing_time': processing_time
        }

        logger.info(f"Successfully extracted {word_count} words from {url}")
        return content, metadata

    except Exception as e:
        logger.error(f"Error extracting content from {url}: {e}")
        raise

def chunk_text(text: str, url: str, heading: str) -> List[Dict]:
    """
    Split long text into smaller chunks with preserved context.

    Args:
        text (str): Full text to be chunked
        url (str): Source URL of the text
        heading (str): Main heading for context

    Returns:
        List[Dict]: Array of chunk objects
    """
    logger.info(f"Chunking text from {url}")

    # Calculate section from URL
    path_parts = urlparse(url).path.strip('/').split('/')
    section = path_parts[0] if path_parts and path_parts[0] else "home"

    # If first part is common web directory name, use the second part
    if section in ['docs', 'blog', 'pages']:
        section = path_parts[1] if len(path_parts) > 1 else section

    # Define chunk size parameters (in characters)
    max_chunk_size = 2000  # Approximate size for 512 tokens
    overlap_size = 200     # Overlap between chunks

    # Split text into sentences to preserve semantic boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""
    current_position = 0

    for sentence in sentences:
        # Check if adding this sentence would exceed the chunk size
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            # If the current chunk is not empty, save it
            if current_chunk.strip():
                word_count = len(current_chunk.split())
                chunk = {
                    'id': f"{url}#{current_position}",
                    'content': current_chunk.strip(),
                    'url': url,
                    'heading': heading,
                    'section': section,
                    'word_count': word_count,
                    'token_count': word_count,  # Approximate token count
                    'source_position': current_position
                }
                chunks.append(chunk)
                current_position += 1

            # Start a new chunk with the current sentence
            current_chunk = sentence

    # Add the last chunk if it has content
    if current_chunk.strip():
        word_count = len(current_chunk.split())
        chunk = {
            'id': f"{url}#{current_position}",
            'content': current_chunk.strip(),
            'url': url,
            'heading': heading,
            'section': section,
            'word_count': word_count,
            'token_count': word_count,  # Approximate token count
            'source_position': current_position
        }
        chunks.append(chunk)

    logger.info(f"Text chunked into {len(chunks)} chunks")
    return chunks

@retry_on_failure(max_retries=3, delay=2, backoff=2)
def embed(text_list: List[str]) -> Tuple[List[List[float]], Dict]:
    """
    Generate embeddings for a list of text chunks using Cohere.

    Args:
        text_list (List[str]): List of text chunks to embed

    Returns:
        Tuple[List[List[float]], Dict]: Array of embedding vectors and processing metadata
    """
    logger.info(f"Generating embeddings for {len(text_list)} text chunks")

    start_time = time.time()

    # Initialize Cohere client
    cohere_api_key = os.getenv('COHERE_API_KEY')
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    co = cohere.Client(cohere_api_key)

    # Process in batches of 96 (Cohere's limit)
    all_embeddings = []
    batch_size = 96

    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i + batch_size]

        try:
            response = co.embed(
                texts=batch,
                model="embed-multilingual-v3.0",  # Using the latest multilingual model
                input_type="search_document"  # Optimal for document search
            )

            batch_embeddings = [embedding for embedding in response.embeddings]
            all_embeddings.extend(batch_embeddings)

            logger.info(f"Processed batch {i//batch_size + 1}/{(len(text_list)-1)//batch_size + 1}")

        except Exception as e:
            logger.error(f"Error embedding batch {i//batch_size + 1}: {e}")
            raise

    total_tokens = sum(len(text.split()) for text in text_list)
    processing_time = time.time() - start_time

    metadata = {
        'model_used': 'embed-multilingual-v3.0',
        'total_tokens': total_tokens,
        'processing_time': processing_time
    }

    logger.info(f"Successfully generated embeddings in {processing_time:.2f}s")
    return all_embeddings, metadata

@retry_on_failure(max_retries=3, delay=1, backoff=2)
def create_collection(collection_name: str) -> Tuple[bool, Dict]:
    """
    Create a new collection in Qdrant Cloud for storing embeddings.

    Args:
        collection_name (str): Name of the collection to create

    Returns:
        Tuple[bool, Dict]: Success status and collection metadata
    """
    logger.info(f"Creating Qdrant collection: {collection_name}")

    # Initialize Qdrant client
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_api_key = os.getenv('QDRANT_API_KEY')

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=120,
        prefer_grpc=False  # Use HTTP for better compatibility
    )

    try:
        # Check if collection already exists
        existing_collections = client.get_collections().collections
        collection_exists = any(col.name == collection_name for col in existing_collections)

        if collection_exists:
            logger.info(f"Collection {collection_name} already exists, using existing collection")
            return True, {
                'collection_name': collection_name,
                'vector_size': 1024,  # Cohere's embed-multilingual-v3.0 vector size
                'distance': 'Cosine',
                'created_at': str(time.time()),
                'status': 'reused'
            }

        # Create new collection
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1024,  # Cohere's embed-multilingual-v3.0 vector size
                distance=models.Distance.COSINE
            )
        )

        logger.info(f"Successfully created collection: {collection_name}")

        return True, {
            'collection_name': collection_name,
            'vector_size': 1024,
            'distance': 'Cosine',
            'created_at': str(time.time()),
            'status': 'created'
        }

    except Exception as e:
        logger.error(f"Error creating collection {collection_name}: {e}")
        raise

@retry_on_failure(max_retries=3, delay=1, backoff=2)
def save_chunk_to_qdrant(chunk_data: Dict) -> Tuple[bool, str, Dict]:
    """
    Save a single chunk with its embedding to Qdrant Cloud.

    Args:
        chunk_data (Dict): Chunk data with embedding

    Returns:
        Tuple[bool, str, Dict]: Success status, point ID, and storage metadata
    """
    logger.info(f"Saving chunk to Qdrant: {chunk_data['id']}")

    # Initialize Qdrant client
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_api_key = os.getenv('QDRANT_API_KEY')

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=120, 
        prefer_grpc=False
    )

    start_time = time.time()

    try:
        # Prepare the payload
        payload = {
            'url': chunk_data['url'],
            'section': chunk_data['section'],
            'heading': chunk_data['heading'],
            'content': chunk_data['content'],
            'word_count': chunk_data['word_count'],
            'token_count': chunk_data['token_count'],
            'source_position': chunk_data['source_position'],
        }

        # Prepare the vector
        vector = chunk_data['embedding']

        # Generate a unique ID for the point
        import uuid
        point_id = str(uuid.uuid4())

        # Upsert the point to Qdrant
        client.upsert(
            collection_name="rag_embeddings",
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )

        processing_time = time.time() - start_time

        metadata = {
            'processing_time': processing_time,
            'collection_name': 'rag_embeddings'
        }

        logger.info(f"Successfully saved chunk {chunk_data['id']} with point ID {point_id}")
        return True, point_id, metadata

    except Exception as e:
        logger.error(f"Error saving chunk to Qdrant: {e}")
        raise

def validate_url(url: str) -> bool:
    """
    Validate if a URL is properly formatted and accessible.

    Args:
        url (str): URL to validate

    Returns:
        bool: True if URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def main():
    """
    Main execution function that orchestrates the complete pipeline:
    1. Discover all URLs from the Docusaurus site
    2. Extract content from each URL
    3. Chunk the content
    4. Generate embeddings
    5. Store in Qdrant
    """
    logger.info("Starting Docusaurus embeddings pipeline")

    # Validate required environment variables
    required_env_vars = ['COHERE_API_KEY', 'QDRANT_URL', 'QDRANT_API_KEY']
    for var in required_env_vars:
        if not os.getenv(var):
            raise ValueError(f"Required environment variable {var} is not set")

    # Get configuration from environment variables with defaults
    base_url = os.getenv('BASE_URL', 'https://tayyaba10.github.io/humanoid_robotics_textbook/')
    chunk_size = int(os.getenv('CHUNK_SIZE', '2000'))  # Character size limit for chunks
    overlap_size = int(os.getenv('OVERLAP_SIZE', '200'))  # Overlap between chunks
    crawl_delay = float(os.getenv('CRAWL_DELAY', '1.0'))  # Delay between requests in seconds
    max_retries = int(os.getenv('MAX_RETRIES', '3'))  # Max retries for failed operations

    # Validate base URL
    if not validate_url(base_url):
        raise ValueError(f"Invalid base URL: {base_url}")

    logger.info(f"Using base URL: {base_url}")
    logger.info(f"Configuration - Chunk size: {chunk_size}, Overlap: {overlap_size}, Delay: {crawl_delay}s, Max retries: {max_retries}")

    # Create the Qdrant collection
    logger.info("Creating Qdrant collection...")
    create_collection("rag_embeddings")

    # Discover all URLs
    logger.info("Discovering URLs...")
    urls, url_metadata = get_all_urls(base_url)
    logger.info(f"Discovered {len(urls)} URLs to process")

    # Process each URL
    processed_count = 0
    failed_count = 0

    for i, url in enumerate(urls):
        try:
            logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

            # Validate URL before processing
            if not validate_url(url):
                logger.warning(f"Invalid URL format: {url}, skipping")
                failed_count += 1
                continue

            # Extract content
            content, content_metadata = extract_text_from_url(url)

            if not content.strip():
                logger.warning(f"No content extracted from {url}, skipping")
                continue

            # Chunk the content
            chunks = chunk_text(content, url, content_metadata['heading'])

            # Process each chunk
            for chunk in chunks:
                # Validate chunk content
                if not chunk.get('content', '').strip():
                    logger.warning(f"Empty chunk content for {url}, skipping")
                    continue

                # Generate embedding for the chunk
                embedding, embed_metadata = embed([chunk['content']])

                # Add embedding to chunk
                chunk['embedding'] = embedding[0]  # Get the first (and only) embedding

                # Save to Qdrant
                success, point_id, save_metadata = save_chunk_to_qdrant(chunk)

                if success:
                    logger.info(f"Successfully processed and saved chunk from {url}")
                else:
                    logger.error(f"Failed to save chunk from {url}")
                    failed_count += 1

            processed_count += 1
            logger.info(f"Successfully processed {url} ({len(chunks)} chunks)")

            # Add a small delay to be respectful to the server
            time.sleep(crawl_delay)

        except Exception as e:
            logger.error(f"Error processing {url}: {e}")
            failed_count += 1
            continue

    logger.info(f"Pipeline completed. Processed: {processed_count}, Failed: {failed_count}")
    logger.info("Docusaurus embeddings pipeline finished successfully")

if __name__ == "__main__":
    main()