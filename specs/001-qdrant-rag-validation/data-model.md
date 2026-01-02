# Data Model: Qdrant RAG Retrieval Pipeline Validation

**Feature**: 001-qdrant-rag-validation
**Date**: 2025-12-25

## Overview

This document defines the data models for the Qdrant RAG retrieval pipeline validation system. The models represent the core entities used for connecting to Qdrant Cloud, executing semantic similarity searches, and validating retrieved content chunks.

## Entity Models

### Query

**Description**: Represents a natural language query submitted to the system for semantic similarity search.

**Fields**:
- `text` (string, required): The natural language query text
- `vector` (array[float], required): The embedding vector representation of the query text
- `metadata` (object, optional): Additional query parameters and context information

**Validation Rules**:
- `text` must be non-empty and not exceed maximum length
- `vector` must have the correct dimensionality to match the Qdrant collection
- `vector` elements must be valid floating-point numbers

**State Transitions**:
- `CREATED` → Query object initialized with text
- `EMBEDDED` → Query text converted to embedding vector
- `PROCESSED` → Query executed against Qdrant collection

### ContentChunk

**Description**: Represents a segment of book content retrieved from the Qdrant vector database based on semantic similarity.

**Fields**:
- `id` (string, required): Unique identifier for the content chunk
- `content` (string, required): The text content of the chunk
- `metadata` (object, required): Source information including URL, section, and heading
- `embedding` (array[float], required): The vector representation of the content
- `similarity_score` (float, required): The similarity score from the search operation

**Validation Rules**:
- `content` must be non-empty
- `embedding` must have the correct dimensionality
- `similarity_score` must be between 0 and 1
- `metadata` must contain required fields (url, section, heading)

**State Transitions**:
- `RETRIEVED` → Content chunk retrieved from Qdrant
- `VALIDATED` → Metadata and content validated
- `SCORED` → Similarity score calculated and assigned

### QdrantConnection

**Description**: Configuration and state for connecting to the Qdrant Cloud service.

**Fields**:
- `host` (string, required): Qdrant Cloud host URL
- `api_key` (string, required): API key for authentication
- `collection_name` (string, required): Name of the target collection
- `connection_timeout` (int, optional): Connection timeout in seconds (default: 30)
- `status` (string, optional): Current connection status (default: "disconnected")

**Validation Rules**:
- `host` must be a valid URL
- `api_key` must be non-empty
- `collection_name` must be non-empty and valid
- `connection_timeout` must be positive

**State Transitions**:
- `CONFIGURED` → Connection parameters set from environment
- `CONNECTING` → Attempting to establish connection
- `CONNECTED` → Successfully connected to Qdrant
- `FAILED` → Connection attempt failed

### RetrievalResult

**Description**: Aggregates the results of a semantic similarity search operation.

**Fields**:
- `query` (object, required): The original Query object used for the search
- `chunks` (array[ContentChunk], required): Array of retrieved content chunks
- `timestamp` (string, required): ISO 8601 timestamp of the retrieval
- `execution_time_ms` (float, required): Time taken to execute the search in milliseconds
- `query_vector` (array[float], optional): The embedding vector used for the search

**Validation Rules**:
- `chunks` array must not be empty
- `execution_time_ms` must be non-negative
- `timestamp` must be a valid ISO 8601 string

**State Transitions**:
- `INITIATED` → Search operation started
- `EXECUTED` → Search completed and results retrieved
- `VALIDATED` → Results validated for accuracy and completeness

### ValidationResult

**Description**: Represents the validation results for retrieved content chunks.

**Fields**:
- `retrieval_result` (object, required): The RetrievalResult being validated
- `metadata_accuracy` (float, required): Percentage of accurate metadata fields (0-100)
- `content_relevance` (float, required): Relevance score of content to query (0-100)
- `validation_timestamp` (string, required): ISO 8601 timestamp of validation
- `issues` (array[object], optional): Array of validation issues found

**Validation Rules**:
- `metadata_accuracy` must be between 0 and 100
- `content_relevance` must be between 0 and 100
- `validation_timestamp` must be a valid ISO 8601 string

**State Transitions**:
- `PENDING` → Validation process initiated
- `PROCESSING` → Validation checks being performed
- `COMPLETED` → All validation checks completed

## Relationships

```
Query 1..* -> * RetrievalResult 1..* -> * ContentChunk
QdrantConnection 1 -> * RetrievalResult
RetrievalResult 1 -> 1 ValidationResult
```

### Query and RetrievalResult
- A Query can initiate multiple RetrievalResult operations over time
- Each RetrievalResult is associated with exactly one Query
- The relationship captures the search history for a given query

### QdrantConnection and RetrievalResult
- A QdrantConnection can be used for multiple RetrievalResult operations
- Each RetrievalResult uses exactly one QdrantConnection
- The relationship ensures connection reuse and pooling

### RetrievalResult and ContentChunk
- A RetrievalResult contains multiple ContentChunk objects
- Each ContentChunk is part of exactly one RetrievalResult
- The relationship represents the results of a single search operation

### RetrievalResult and ValidationResult
- A RetrievalResult has exactly one ValidationResult
- Each ValidationResult is associated with exactly one RetrievalResult
- The relationship captures the validation status of the retrieval

## Data Flow

1. **Query Creation**: User provides natural language query
2. **Embedding**: Query text is converted to embedding vector
3. **Connection**: QdrantConnection is established using configuration
4. **Retrieval**: Semantic similarity search is performed against Qdrant
5. **Result Assembly**: RetrievalResult is created with ContentChunk array
6. **Validation**: ValidationResult is generated for the RetrievalResult
7. **Response**: Validated results are returned to the user

## Constraints

### Dimensionality Constraint
- All embedding vectors (queries and stored content) must have the same dimensionality
- This is determined by the Cohere embedding model used for the stored content
- Query embeddings must be generated using the same model

### Performance Constraint
- Retrieval operations must complete within 1 second for 95% of requests
- This constraint drives optimization decisions in the implementation

### Metadata Integrity Constraint
- All ContentChunk objects must have complete and accurate metadata
- Missing or incorrect metadata should be flagged during validation

## Indexing Strategy

### Qdrant Collection Indexes
- Vector index on the embedding field for similarity search
- Index on metadata fields (URL, section, heading) for filtering
- Composite index on frequently queried metadata combinations

### Query Optimization
- Use pre-filtering where possible to reduce search space
- Implement result caching for frequently requested content
- Optimize vector search parameters for accuracy vs performance trade-offs