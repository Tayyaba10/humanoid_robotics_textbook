# API Contracts: Docusaurus Embeddings System

## 1. Core Functions Specification (main.py)

### 1.1 get_all_urls(base_url)
**Purpose**: Discover and return all accessible URLs from the Docusaurus website

**Inputs**:
- `base_url` (string): Base URL of the Docusaurus site (e.g., "https://tayyaba10.github.io/humanoid_robotics_textbook/")

**Outputs**:
- `urls` (array of strings): List of all discovered URLs from the site
- `metadata` (object): Additional information about the crawl
  - `total_urls` (integer): Total number of URLs discovered
  - `crawl_time` (number): Time taken to complete the crawl in seconds
  - `errors` (array): List of URLs that failed to be processed

**Errors**:
- `InvalidBaseUrlError`: When the base_url is malformed or inaccessible
- `NetworkError`: When network requests fail during crawling
- `PermissionError`: When the site blocks crawling attempts

**Example**:
```python
urls, metadata = get_all_urls("https://tayyaba10.github.io/humanoid_robotics_textbook/")
# urls = ["https://tayyaba10.github.io/humanoid_robotics_textbook/intro", ...]
```

### 1.2 extract_text_from_url(url)
**Purpose**: Extract and clean text content from a specific URL

**Inputs**:
- `url` (string): URL to extract content from

**Outputs**:
- `content` (string): Cleaned, extracted text content
- `metadata` (object): Additional information about the page
  - `title` (string): Page title
  - `heading` (string): Main heading of the content
  - `section` (string): Docusaurus section/category
  - `description` (string): Meta description if available
  - `word_count` (integer): Number of words in extracted content
  - `processing_time` (number): Time taken to process the page

**Errors**:
- `UrlNotFoundError`: When the URL returns 404 or similar error
- `ContentExtractionError`: When content cannot be properly extracted
- `NetworkError`: When the URL request fails

**Example**:
```python
content, metadata = extract_text_from_url("https://tayyaba10.github.io/humanoid_robotics_textbook/intro")
# content = "Introduction to humanoid robotics..."
# metadata = {"title": "Introduction", "heading": "What are Humanoid Robots?", ...}
```

### 1.3 chunk_text(text, url, heading)
**Purpose**: Split long text into smaller chunks with preserved context

**Inputs**:
- `text` (string): Full text to be chunked
- `url` (string): Source URL of the text
- `heading` (string): Main heading for context

**Outputs**:
- `chunks` (array of objects): Array of chunk objects
  - `id` (string): Unique identifier for the chunk
  - `content` (string): Chunk text content
  - `url` (string): Source URL
  - `heading` (string): Heading context
  - `section` (string): Docusaurus section
  - `word_count` (integer): Number of words in chunk
  - `token_count` (integer): Number of tokens in chunk
  - `source_position` (integer): Position in original document

**Constraints**:
- Maximum chunk size: 512 tokens
- Minimum chunk size: 10 words
- Overlap between chunks: 50 tokens maximum
- Preserve semantic boundaries (don't split sentences)

**Example**:
```python
chunks = chunk_text("Long text content...", "https://example.com/page", "Main Heading")
# chunks = [
#   {
#     "id": "uuid-1",
#     "content": "First chunk of content...",
#     "url": "https://example.com/page",
#     "heading": "Main Heading",
#     "section": "introduction",
#     "word_count": 85,
#     "token_count": 95,
#     "source_position": 0
#   },
#   ...
# ]
```

### 1.4 embed(text_list)
**Purpose**: Generate embeddings for a list of text chunks using Cohere

**Inputs**:
- `text_list` (array of strings): List of text chunks to embed

**Outputs**:
- `embeddings` (array of arrays): Array of embedding vectors
- `metadata` (object): Processing information
  - `model_used` (string): Name of the embedding model
  - `total_tokens` (integer): Total tokens processed
  - `processing_time` (number): Time taken to generate embeddings

**Errors**:
- `ApiKeyError`: When Cohere API key is invalid or missing
- `RateLimitError`: When API rate limits are exceeded
- `EmbeddingError`: When embedding generation fails

**Constraints**:
- Maximum batch size: 96 texts per request (Cohere limit)
- Vector dimension: 1024 (for embed-multilingual-v3.0 model)
- Input text length: Maximum 5,120 tokens per text

**Example**:
```python
embeddings, metadata = embed(["text chunk 1", "text chunk 2"])
# embeddings = [[0.1, 0.3, ...], [0.4, 0.2, ...]]  # Each with 1024 dimensions
```

### 1.5 create_collection(collection_name)
**Purpose**: Create a new collection in Qdrant Cloud for storing embeddings

**Inputs**:
- `collection_name` (string): Name of the collection to create ("rag_embeddings")

**Outputs**:
- `success` (boolean): Whether the collection was created successfully
- `metadata` (object): Collection information
  - `collection_name` (string): Name of the created collection
  - `vector_size` (integer): Size of vectors in the collection (1024)
  - `distance` (string): Distance metric used (cosine)
  - `created_at` (timestamp): When the collection was created

**Errors**:
- `ConnectionError`: When unable to connect to Qdrant Cloud
- `AuthenticationError`: When Qdrant credentials are invalid
- `CollectionExistsError`: When collection already exists

**Example**:
```python
success, metadata = create_collection("rag_embeddings")
# success = True
# metadata = {"collection_name": "rag_embeddings", "vector_size": 1024, ...}
```

### 1.6 save_chunk_to_qdrant(chunk_data)
**Purpose**: Save a single chunk with its embedding to Qdrant Cloud

**Inputs**:
- `chunk_data` (object): Chunk data with embedding
  - `id` (string): Unique chunk identifier
  - `content` (string): Text content
  - `url` (string): Source URL
  - `section` (string): Docusaurus section
  - `heading` (string): Heading context
  - `embedding` (array of numbers): Vector representation
  - `word_count` (integer): Word count
  - `token_count` (integer): Token count
  - `source_position` (integer): Position in original document

**Outputs**:
- `success` (boolean): Whether the chunk was saved successfully
- `point_id` (string): ID assigned by Qdrant for the stored point
- `metadata` (object): Storage information
  - `processing_time` (number): Time taken to store
  - `collection_name` (string): Name of the target collection

**Errors**:
- `ConnectionError`: When unable to connect to Qdrant Cloud
- `ValidationError`: When chunk data doesn't meet schema requirements
- `StorageError`: When storage operation fails

**Example**:
```python
chunk_data = {
    "id": "chunk-123",
    "content": "Sample content...",
    "url": "https://example.com/page",
    "embedding": [0.1, 0.3, ...],
    # ... other fields
}
success, point_id, metadata = save_chunk_to_qdrant(chunk_data)
# success = True
# point_id = "qdrant-assigned-id"
```

## 2. Main Execution Function

### 2.1 main()
**Purpose**: Orchestrate the complete pipeline from URL discovery to vector storage

**Inputs**: None (reads configuration from environment variables)

**Outputs**: None (writes results to Qdrant Cloud)

**Environment Variables Required**:
- `COHERE_API_KEY`: Cohere API key for embeddings
- `QDRANT_URL`: Qdrant Cloud URL
- `QDRANT_API_KEY`: Qdrant Cloud API key
- `BASE_URL`: Target Docusaurus site URL (default: "https://tayyaba10.github.io/humanoid_robotics_textbook/")

**Execution Flow**:
1. Validate required environment variables
2. Create Qdrant collection
3. Discover all URLs from the base site
4. For each URL: extract content, chunk text, generate embeddings
5. Store each chunk with embedding in Qdrant
6. Log progress and final statistics

**Error Handling**:
- Retry failed operations with exponential backoff
- Continue processing other URLs if one fails
- Log all errors for debugging
- Provide summary of successful and failed operations

## 3. Data Contract Validation

### 3.1 Input Validation
- All string inputs must be properly encoded (UTF-8)
- URLs must pass validation checks (proper format, accessible)
- Text content must not exceed size limits for APIs
- Environment variables must be present and valid

### 3.2 Output Validation
- Embedding vectors must have correct dimensions (1024)
- All required metadata fields must be present
- Chunk content must meet minimum quality requirements
- Unique identifiers must be properly formatted

## 4. Performance Contracts

### 4.1 Timeouts
- HTTP requests: 30 seconds per request
- Embedding API calls: 60 seconds per batch
- Qdrant operations: 10 seconds per operation

### 4.2 Rate Limits
- Web crawling: 1-2 requests per second (respectful)
- Cohere API: As per account limits
- Qdrant Cloud: As per account limits

### 4.3 Resource Usage
- Memory usage: Should not exceed 1GB during processing
- Concurrent operations: Limited to 5-10 parallel operations
- Disk usage: Minimal (processing in memory)