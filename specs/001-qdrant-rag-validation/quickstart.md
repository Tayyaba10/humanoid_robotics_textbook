# Quickstart Guide: Qdrant RAG Retrieval Pipeline Validation

**Feature**: 001-qdrant-rag-validation
**Date**: 2025-12-25

## Overview

This guide provides a quick start for setting up and running the Qdrant RAG retrieval pipeline validation system. The system connects to Qdrant Cloud to validate semantic similarity searches against pre-generated Cohere embeddings of book content.

## Prerequisites

- Python 3.11 or higher
- UV package manager
- Access to Qdrant Cloud instance
- Cohere API key for embedding generation
- Pre-generated embeddings in Qdrant collection

## Environment Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies using UV**:
   ```bash
   cd backend
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install qdrant-client cohere python-dotenv requests pytest
   ```

3. **Set up environment variables**:
   Create a `.env` file in the backend directory:
   ```env
   QDRANT_HOST=https://your-cluster-url.qdrant.tech
   QDRANT_API_KEY=your-qdrant-api-key
   COHERE_API_KEY=your-cohere-api-key
   COLLECTION_NAME=your-embeddings-collection
   ```

## Running the Validation

1. **Run the connection test**:
   ```bash
   python -c "
   from src.services.qdrant_connection import QdrantConnection
   conn = QdrantConnection.from_env()
   print('Connection status:', conn.test_connection())
   "
   ```

2. **Execute a sample query**:
   ```bash
   python -c "
   from src.services.retrieval_service import RetrievalService
   service = RetrievalService.from_env()
   result = service.search('Sample query about book content', top_k=5)
   print('Retrieved chunks:', len(result.chunks))
   for chunk in result.chunks:
       print(f'- Score: {chunk.similarity_score:.3f}, Content: {chunk.content[:100]}...')
   "
   ```

3. **Run validation tests**:
   ```bash
   pytest tests/validation/
   ```

## Validation Examples

### Basic Semantic Search
```python
from src.services.retrieval_service import RetrievalService

service = RetrievalService.from_env()
result = service.search('What does the book say about machine learning?', top_k=3)

for chunk in result.chunks:
    print(f"Similarity: {chunk.similarity_score}")
    print(f"Content: {chunk.content}")
    print(f"Source: {chunk.metadata['url']}")
    print("---")
```

### Metadata Validation
```python
from src.services.validation_service import ValidationService

validator = ValidationService()
validation_result = validator.validate_retrieval(result)

print(f"Metadata accuracy: {validation_result.metadata_accuracy}%")
print(f"Content relevance: {validation_result.content_relevance}%")
```

## API Usage

### Starting the API Server
```bash
cd backend
uv run python -m src.api.main
```

### Making API Requests
```bash
curl -X POST http://localhost:8000/api/retrieve \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main concept discussed in chapter 3?",
    "top_k": 5
  }'
```

## Testing the System

1. **Run unit tests**:
   ```bash
   pytest tests/unit/
   ```

2. **Run integration tests**:
   ```bash
   pytest tests/integration/
   ```

3. **Run performance tests**:
   ```bash
   pytest tests/performance/
   ```

## Configuration Options

### Connection Settings
- `QDRANT_HOST`: Qdrant Cloud instance URL
- `QDRANT_API_KEY`: Authentication key for Qdrant
- `COLLECTION_NAME`: Name of the embeddings collection
- `CONNECTION_TIMEOUT`: Connection timeout in seconds (default: 30)

### Query Settings
- `TOP_K`: Number of results to return (default: 5)
- `SEARCH_LIMIT`: Maximum number of candidates to consider (default: 1000)
- `SCORE_THRESHOLD`: Minimum similarity score for results (default: 0.0)

## Troubleshooting

### Common Issues

1. **Connection failures**:
   - Verify QDRANT_HOST and QDRANT_API_KEY are correct
   - Check network connectivity to Qdrant Cloud
   - Ensure the collection exists and is accessible

2. **Empty results**:
   - Verify the collection contains embeddings
   - Check that query embeddings match stored embedding dimensions
   - Ensure the Cohere model matches the one used for stored embeddings

3. **Performance issues**:
   - Monitor query execution times
   - Consider adjusting search parameters
   - Check Qdrant Cloud instance performance

### Validation Logs
Check the validation logs for detailed information about retrieval accuracy:
- `logs/validation.log`: Validation results and metrics
- `logs/retrieval.log`: Query execution details
- `logs/errors.log`: Error information and troubleshooting

## Next Steps

1. Customize the validation tests for your specific book content
2. Adjust performance parameters based on your requirements
3. Set up monitoring for production usage
4. Implement additional validation checks as needed