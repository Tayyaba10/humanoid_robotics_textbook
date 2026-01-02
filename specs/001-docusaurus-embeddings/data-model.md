# Data Model: Docusaurus Embeddings for Humanoid Robotics Textbook

## 1. Core Entities

### 1.1 Content Chunk
The primary entity representing a piece of content from the Docusaurus site.

**Fields**:
- `id` (string): Unique identifier for the chunk (UUID v4 format)
- `url` (string): Source URL of the original content
- `section` (string): Docusaurus section/category name
- `heading` (string): Primary heading of the content section
- `content` (string): Cleaned, processed text content (max 512 tokens)
- `embedding` (array of numbers): Vector representation from Cohere model
- `created_at` (timestamp): When the chunk was created
- `updated_at` (timestamp): When the chunk was last updated
- `word_count` (integer): Number of words in the content
- `token_count` (integer): Number of tokens in the content
- `source_position` (integer): Position of this chunk in the original document

**Relationships**:
- One-to-many with Document (a document contains multiple chunks)
- One-to-many with Metadata (chunk has additional metadata)

**Validation Rules**:
- `id` must be a valid UUID v4
- `url` must be a valid URL format
- `content` length must be between 10 and 4000 characters
- `embedding` must be an array of 1024 numbers (for Cohere embed-multilingual-v3.0)
- `word_count` and `token_count` must be positive integers

### 1.2 Document Metadata
Metadata for the original document before chunking.

**Fields**:
- `id` (string): Unique identifier (UUID v4 format)
- `original_url` (string): Source URL of the document
- `title` (string): Document title/heading
- `description` (string): Document description from meta tags
- `author` (string): Document author (if available)
- `tags` (array of strings): Docusaurus tags associated with the document
- `last_modified` (timestamp): Last modification date of the source
- `language` (string): Document language code (e.g., 'en', 'es')
- `word_count` (integer): Total word count of the original document
- `chunk_count` (integer): Number of chunks created from this document

**Relationships**:
- One-to-many with Content Chunk (document produces multiple chunks)

### 1.3 Processing Log
Record of the processing pipeline execution.

**Fields**:
- `id` (string): Unique identifier (UUID v4 format)
- `pipeline_name` (string): Name of the processing pipeline ('docusaurus-crawler')
- `start_time` (timestamp): When the pipeline started
- `end_time` (timestamp): When the pipeline completed
- `status` (string): Current status ('running', 'completed', 'failed', 'partial')
- `processed_urls` (integer): Number of URLs successfully processed
- `failed_urls` (integer): Number of URLs that failed to process
- `total_chunks` (integer): Total number of chunks created
- `errors` (array of objects): List of errors encountered during processing

## 2. Vector Database Schema (Qdrant)

### 2.1 Collection Configuration
- **Collection Name**: `rag_embeddings`
- **Vector Size**: 1024 (for Cohere embed-multilingual-v3.0)
- **Distance**: Cosine
- **On Disk**: True (for large datasets)

### 2.2 Payload Schema
The payload in Qdrant will store the metadata for each chunk:

```json
{
  "id": "uuid",
  "url": "string",
  "section": "string",
  "heading": "string",
  "content": "string",
  "word_count": "integer",
  "token_count": "integer",
  "source_position": "integer",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### 2.3 Indexing Strategy
- **Indexed Fields**: `url`, `section`, `heading` for fast filtering
- **Full-text Search**: Enabled on `content` field for keyword search
- **Composite Indexes**: Combination of `section` and `heading` for category-based queries

## 3. State Transitions

### 3.1 Content Chunk States
- **Created**: Chunk has been generated but not yet embedded
- **Embedded**: Chunk has been processed by embedding model
- **Stored**: Chunk has been saved to vector database
- **Indexed**: Chunk is available for search queries

### 3.2 Processing Pipeline States
- **Initializing**: Pipeline is starting up
- **Discovering URLs**: Crawling and finding all pages
- **Extracting Content**: Processing each URL
- **Chunking Text**: Splitting content into chunks
- **Generating Embeddings**: Creating vector representations
- **Storing Chunks**: Saving to vector database
- **Completed**: Pipeline finished successfully
- **Failed**: Pipeline encountered unrecoverable error

## 4. Data Validation Rules

### 4.1 Content Quality Rules
- Minimum content length: 10 words
- Maximum chunk size: 512 tokens
- Content must not be purely navigational elements
- Preserve educational context in chunks

### 4.2 Metadata Completeness
- URL must be present and valid
- Section and heading must be extracted
- Creation timestamp must be set
- Word and token counts must be calculated

### 4.3 Embedding Validation
- Embedding vector must have exactly 1024 dimensions
- All vector values must be finite numbers
- No null or undefined values in vector array

## 5. Data Relationships

### 5.1 Hierarchical Structure
```
Document (1) -> Content Chunks (0..n)
  -> Metadata
  -> Processing Log
```

### 5.2 Cross-Reference Relationships
- Chunks from same URL grouped by `url` field
- Chunks from same section grouped by `section` field
- Related chunks identified through semantic similarity (vector distance)