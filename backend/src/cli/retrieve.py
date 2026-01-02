#!/usr/bin/env python3
"""
RAG Retrieval CLI Tool

Command-line interface tool for retrieving top-k relevant content from a vector database
for a user-provided query. Returns results with content, source, chunk index, and similarity scores.
"""
import argparse
import logging
import os
import sys
from typing import Optional

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
except ImportError:
    print("Error: qdrant-client is not installed. Please install it using 'pip install qdrant-client'", file=sys.stderr)
    sys.exit(1)

try:
    import cohere
except ImportError:
    print("Error: cohere is not installed. Please install it using 'pip install cohere'", file=sys.stderr)
    sys.exit(1)

# Set up logging for connection attempts and retrieval requests
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RAGRetrievalError(Exception):
    """Custom exception for RAG retrieval errors."""
    pass


class ConfigurationError(RAGRetrievalError):
    """Exception for configuration-related errors."""
    pass


class ValidationError(RAGRetrievalError):
    """Exception for validation-related errors."""
    pass


def setup_arg_parser():
    """Set up argument parser for the CLI tool."""
    parser = argparse.ArgumentParser(
        description="Retrieve top-k relevant content from a vector database for a user query"
    )
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="User input query string to search for"
    )
    parser.add_argument(
        "--top_k",
        type=int,
        default=5,
        help="Number of top results to return (default: 5, min: 1, max: 100)"
    )
    return parser


def load_configuration() -> dict:
    """
    Load and validate environment configuration.

    Returns:
        dict: Configuration dictionary with QDRANT_HOST, QDRANT_API_KEY,
              COLLECTION_NAME, and COHERE_API_KEY
    """
    required_vars = ["QDRANT_HOST", "QDRANT_API_KEY", "COLLECTION_NAME", "COHERE_API_KEY"]
    config = {}

    for var in required_vars:
        value = os.getenv(var)
        if not value:
            raise ConfigurationError(f"Missing required environment variable: {var}")

        # Trim whitespace and quotes from environment variables
        value = value.strip().strip('"\'')
        if not value:
            raise ConfigurationError(f"Environment variable {var} is empty after trimming")

        config[var.lower()] = value

    return config


def validate_host_format(host: str) -> bool:
    """
    Validate the format of a host URL.

    Args:
        host: Host URL string to validate

    Returns:
        bool: True if format is valid, False otherwise
    """
    import re
    # Check if it's a proper URL format
    if host.startswith('https://') or host.startswith('http://'):
        # Use regex to validate URL format
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(host) is not None
    else:
        # Check if it's a simple host:port format
        host_pattern = re.compile(
            r'^(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'  # IP
            r'(?::\d+)?$', re.IGNORECASE)  # optional port
        return host_pattern.match(host) is not None


def connect_to_qdrant(config: dict) -> QdrantClient:
    """
    Implement Qdrant client connection with authentication.

    Args:
        config: Configuration dictionary containing QDRANT_HOST and QDRANT_API_KEY

    Returns:
        QdrantClient: Connected Qdrant client instance
    """
    try:
        # Validate host format
        host = config['qdrant_host']
        if not validate_host_format(host):
            raise ConfigurationError(f"Invalid QDRANT_HOST format: {host}")

        # Validate API key format
        api_key = config['qdrant_api_key']
        if not api_key or not isinstance(api_key, str) or len(api_key.strip()) == 0:
            raise ConfigurationError("Invalid QDRANT_API_KEY: API key is empty or invalid")

        if host.startswith('https://') or host.startswith('http://'):
            # It's a full URL, extract the host
            from urllib.parse import urlparse
            parsed = urlparse(host)
            client = QdrantClient(
                url=parsed.netloc,
                api_key=api_key,
                https=True if parsed.scheme == 'https' else False,
                timeout=10  # Add timeout for connection
            )
        else:
            # It's just a host, connect directly
            client = QdrantClient(
                url=host,
                api_key=api_key,
                timeout=10  # Add timeout for connection
            )

        # Test the connection by trying to list collections
        client.get_collections()
        logger.info("Successfully connected to Qdrant")
        return client
    except ConfigurationError:
        # Re-raise configuration errors as they are
        raise
    except Exception as e:
        raise ConfigurationError(f"Failed to connect to Qdrant: {str(e)}")


def verify_collection_exists(client: QdrantClient, collection_name: str) -> bool:
    """
    Implement collection existence verification.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection to verify

    Returns:
        bool: True if collection exists, False otherwise
    """
    try:
        collections = client.get_collections()
        collection_names = [collection.name for collection in collections.collections]

        if collection_name not in collection_names:
            available_collections = ", ".join(collection_names) if collection_names else "No collections found"
            raise ConfigurationError(
                f"Collection '{collection_name}' does not exist in Qdrant. "
                f"Available collections: {available_collections}"
            )

        logger.info(f"Collection '{collection_name}' verified to exist")
        return True
    except ConfigurationError:
        # Re-raise configuration errors as they are
        raise
    except Exception as e:
        raise ConfigurationError(f"Failed to verify collection existence: {str(e)}")


def connect_to_cohere(config: dict) -> cohere.Client:
    """
    Implement Cohere client connection with authentication.

    Args:
        config: Configuration dictionary containing COHERE_API_KEY

    Returns:
        cohere.Client: Connected Cohere client instance
    """
    try:
        api_key = config['cohere_api_key']

        # Validate API key format (basic check - should be a non-empty string)
        if not api_key or not isinstance(api_key, str) or len(api_key.strip()) == 0:
            raise ConfigurationError("Invalid COHERE_API_KEY: API key is empty or invalid")

        client = cohere.Client(api_key)
        # Test the connection by making a simple API call
        client.embed(texts=["test"], model="embed-multilingual-v2.0")
        logger.info("Successfully connected to Cohere")
        return client
    except ConfigurationError:
        # Re-raise configuration errors as they are
        raise
    except Exception as e:
        raise ConfigurationError(f"Failed to connect to Cohere: {str(e)}")


def generate_query_embeddings(client: cohere.Client, query: str) -> list:
    """
    Implement query embedding generation using Cohere.

    Args:
        client: Cohere client instance
        query: Query string to embed

    Returns:
        list: Embedding vector for the query
    """
    try:
        response = client.embed(texts=[query], model="embed-multilingual-v2.0")
        embeddings = response.embeddings
        if embeddings and len(embeddings) > 0:
            logger.info("Query embedding generated successfully")
            return embeddings[0]  # Return the first (and only) embedding
        else:
            raise RAGRetrievalError("Failed to generate embeddings for the query")
    except Exception as e:
        raise RAGRetrievalError(f"Failed to generate query embeddings: {str(e)}")


def retry_with_backoff(func, max_retries=3, delay=1, backoff=2):
    """
    Implement retry logic with exponential backoff for transient failures.

    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries (in seconds)
        backoff: Multiplier for delay after each retry

    Returns:
        Result of the function call
    """
    import time
    current_delay = delay

    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries:
                # If we've exhausted retries, raise the exception
                raise e

            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {current_delay} seconds...")
            time.sleep(current_delay)
            current_delay *= backoff

    # This line should never be reached
    raise RAGRetrievalError("Retry function failed unexpectedly")


def perform_semantic_search(client: QdrantClient, collection_name: str, query_vector: list, top_k: int) -> list:
    """
    Implement semantic search in Qdrant collection.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection to search in
        query_vector: Query embedding vector
        top_k: Number of top results to return

    Returns:
        list: List of search results with payload and similarity scores
    """
    # Define the search operation for retry logic
    def search_operation():
        # Based on the error logs, the 'search' method doesn't exist in this version
        # In older versions of qdrant-client, search functionality is accessed differently
        # The most common method in older versions is search_points
        try:
            # Try search_points first (common in older versions)
            search_results = client.search_points(
                collection_name=collection_name,
                vector=query_vector,  # Using 'vector' parameter which is common in older versions
                limit=top_k,
                with_payload=True
            )
            logger.info(f"Semantic search completed using search_points method, found {len(search_results)} results")
            return search_results
        except AttributeError:
            # If search_points doesn't exist, try the main search method (newer versions)
            try:
                search_results = client.search(
                    collection_name=collection_name,
                    query_vector=query_vector,
                    limit=top_k,
                    with_payload=True
                )
                logger.info(f"Semantic search completed using search method, found {len(search_results)} results")
                return search_results
            except AttributeError:
                # If neither exists, try points.search
                try:
                    search_results = client.points.search(
                        collection_name=collection_name,
                        vector=query_vector,  # Using 'vector' parameter
                        limit=top_k,
                        with_payload=True
                    )
                    logger.info(f"Semantic search completed using points.search method, found {len(search_results)} results")
                    return search_results
                except AttributeError:
                    # If none of the above work, try search_batch
                    try:
                        # For batch search operations
                        search_results = client.search_batch(
                            collection_name=collection_name,
                            requests=[{
                                "vector": query_vector,
                                "limit": top_k,
                                "with_payload": True
                            }]
                        )
                        if search_results and len(search_results) > 0:
                            logger.info(f"Semantic search completed using search_batch method, found {len(search_results[0])} results")
                            return search_results[0]
                        else:
                            raise RAGRetrievalError("No results returned from search_batch")
                    except AttributeError:
                        # If search_batch doesn't exist either, try another approach
                        try:
                            # Some versions use a different approach with Query
                            search_result = client.query(
                                collection_name=collection_name,
                                query=query_vector,
                                limit=top_k,
                                with_payload=True
                            )
                            logger.info(f"Semantic search completed using query method, found {len(search_result)} results")
                            return search_result
                        except AttributeError:
                            # If all methods fail, raise an error
                            raise RAGRetrievalError(
                                "Failed to perform semantic search: No suitable search method found in the qdrant-client version. "
                                "Available methods: " + str([m for m in dir(client) if 'search' in m.lower() or 'query' in m.lower()])
                            )

    # Perform the search with retry logic
    try:
        search_results = retry_with_backoff(search_operation)
        return search_results
    except Exception as e:
        raise RAGRetrievalError(f"Failed to perform semantic search: {str(e)}")


def format_results(search_results: list) -> list:
    """
    Implement result formatting according to specified output format.

    Args:
        search_results: List of search results from Qdrant

    Returns:
        list: Formatted results with content, source, chunk index, and similarity scores
    """
    formatted_results = []

    for i, result in enumerate(search_results):
        # Extract the required information from the result
        # Assuming the payload contains 'content', 'source', 'chunk_index' fields
        payload = result.payload if result.payload else {}

        # Extract fields with defaults
        content_text = payload.get('content', 'No content available')
        source_document = payload.get('source', 'Unknown source')
        chunk_index = payload.get('chunk_index', -1)
        similarity_score = result.score if result.score is not None else 0.0

        formatted_result = {
            'content_text': content_text,
            'source_document': source_document,
            'chunk_index': chunk_index,
            'similarity_score': similarity_score
        }

        formatted_results.append(formatted_result)

    logger.info(f"Formatted {len(formatted_results)} results for display")
    return formatted_results


def display_results(formatted_results: list):
    """
    Implement result display with score, source, chunk, and text.

    Args:
        formatted_results: List of formatted results to display
    """
    for i, result in enumerate(formatted_results, 1):
        print(f"[{i}] Score: {result['similarity_score']:.2f}")
        print(f"    Source: {result['source_document']}")
        print(f"    Chunk: {result['chunk_index']}")
        print(f"    Text: {result['content_text'][:100]}{'...' if len(result['content_text']) > 100 else ''}")
        print()  # Empty line between results


def main():
    """Main function for the RAG retrieval CLI tool."""
    start_time = None
    try:
        logger.info("Starting RAG retrieval process")
        start_time = __import__('time').time()  # Import time to measure performance

        # Set up argument parser
        parser = setup_arg_parser()
        args = parser.parse_args()

        logger.info(f"Processing query: '{args.query[:50]}{'...' if len(args.query) > 50 else ''}' with top_k={args.top_k}")

        # Validate input parameters
        if not args.query or not args.query.strip():
            print("Error: Query cannot be empty or all whitespace", file=sys.stderr)
            sys.exit(2)  # Invalid arguments exit code

        if len(args.query.strip()) > 1000:
            print("Error: Query is too long (maximum 1000 characters)", file=sys.stderr)
            sys.exit(2)  # Invalid arguments exit code

        if args.top_k < 1 or args.top_k > 100:
            print("Error: top_k must be a positive integer between 1 and 100", file=sys.stderr)
            sys.exit(2)  # Invalid arguments exit code

        # Load configuration
        config = load_configuration()
        logger.info("Configuration loaded successfully")

        # Connect to Qdrant
        logger.info("Connecting to Qdrant...")
        qdrant_client = connect_to_qdrant(config)

        # Verify collection exists
        logger.info(f"Verifying collection '{config['collection_name']}' exists...")
        verify_collection_exists(qdrant_client, config['collection_name'])

        # Connect to Cohere
        logger.info("Connecting to Cohere...")
        cohere_client = connect_to_cohere(config)

        # Generate query embeddings
        logger.info("Generating query embeddings...")
        query_embedding = generate_query_embeddings(cohere_client, args.query)

        # Perform semantic search in Qdrant
        logger.info(f"Performing semantic search in collection '{config['collection_name']}'...")
        search_results = perform_semantic_search(qdrant_client, config['collection_name'], query_embedding, args.top_k)

        # Format the search results
        logger.info("Formatting search results...")
        formatted_results = format_results(search_results)

        # Display the formatted results
        logger.info(f"Displaying {len(formatted_results)} results")
        display_results(formatted_results)

        # Calculate and log execution time
        end_time = __import__('time').time()
        execution_time = end_time - start_time
        logger.info(f"RAG retrieval completed successfully in {execution_time:.2f} seconds")

        # Verify performance requirements
        if execution_time > 5.0:
            logger.warning(f"Performance requirement exceeded: took {execution_time:.2f} seconds (limit: 5 seconds)")
        else:
            logger.info(f"Performance requirement met: {execution_time:.2f} seconds < 5 seconds")

    except ConfigurationError as e:
        if start_time:
            end_time = __import__('time').time()
            execution_time = end_time - start_time
            logger.error(f"RAG retrieval failed after {execution_time:.2f} seconds: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(4)  # Authentication error exit code
    except ValidationError as e:
        if start_time:
            end_time = __import__('time').time()
            execution_time = end_time - start_time
            logger.error(f"RAG retrieval failed after {execution_time:.2f} seconds: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)  # Invalid arguments exit code
    except Exception as e:
        if start_time:
            end_time = __import__('time').time()
            execution_time = end_time - start_time
            logger.error(f"RAG retrieval failed after {execution_time:.2f} seconds: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)  # General error exit code


if __name__ == "__main__":
    main()