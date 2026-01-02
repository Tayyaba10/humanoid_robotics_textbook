# Data Model: RAG Retrieval CLI Tool

**Feature**: 001-rag-retrieval
**Created**: 2025-12-26
**Status**: Draft

## Entities

### Query
- **Description**: User-provided search string that will be converted to embeddings for semantic search
- **Fields**:
  - text: string (the actual query text)
  - embedding: list[float] (vector representation of the query)
- **Validation**:
  - Must not be empty
  - Length should be reasonable (not exceed API limits)
- **State Transitions**: plain text → encoded embedding

### RetrievalResult
- **Description**: Structured data containing content text, source document, chunk index, and similarity score for each result
- **Fields**:
  - content_text: string (the actual content text)
  - source_document: string (source file or document identifier)
  - chunk_index: integer (index of the chunk within the source)
  - similarity_score: float (similarity score between query and result)
- **Validation**:
  - content_text must not be empty
  - similarity_score must be between 0 and 1
  - chunk_index must be non-negative
- **State Transitions**: None (immutable result object)

### EnvironmentConfiguration
- **Description**: Set of variables (database host URL, database API key, collection name, embedding service API key) that configure the system
- **Fields**:
  - qdrant_host: string (URL for Qdrant service)
  - qdrant_api_key: string (API key for Qdrant authentication)
  - collection_name: string (name of the collection to search)
  - cohere_api_key: string (API key for Cohere service)
- **Validation**:
  - All fields must be present
  - URLs must be valid
  - API keys must not be empty after trimming
- **State Transitions**: None (configuration is loaded once at startup)

## Relationships

```
Query --(encoded to)--> Embedding Vector --(searched in)--> Qdrant Collection
Qdrant Collection --(returns)--> [RetrievalResult]
EnvironmentConfiguration --(used by)--> Query Processor
```

## State Diagram

### Query Processing Flow:
```
[User Input] --> [Validation] --> [Embedding Generation] --> [Search Request] --> [Results Processing] --> [Formatted Output]
```

## Data Validation Rules

1. **Query Validation**:
   - Minimum length: 1 character
   - Maximum length: 1000 characters (to prevent API limits)
   - Cannot be all whitespace

2. **Top-K Validation**:
   - Must be positive integer
   - Maximum value: 100 (to prevent excessive resource usage)

3. **Configuration Validation**:
   - All environment variables must be present
   - URLs must have proper format
   - API keys must be non-empty after trimming whitespace

4. **Result Validation**:
   - Each result must have content_text, source_document, and similarity_score
   - Similarity scores must be between 0 and 1