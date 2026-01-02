# RAG Retrieval CLI Tool

Command-line interface tool for retrieving top-k relevant content from a vector database for a user-provided query. Returns results with content, source, chunk index, and similarity scores.

## Usage

### Basic Usage
```bash
python -m backend.src.cli.retrieve --query "What is humanoid robotics?" --top_k 5
```

### With Default Top-K
```bash
python -m backend.src.cli.retrieve --query "How do robots navigate?"
```

### Environment Configuration
```bash
export QDRANT_HOST="https://your-cluster.qdrant.tech:6333"
export QDRANT_API_KEY="your-api-key"
export COLLECTION_NAME="robotics_docs"
export COHERE_API_KEY="your-cohere-api-key"
python -m backend.src.cli.retrieve --query "locomotion algorithms" --top_k 3
```

## Arguments

### Required Arguments
- `--query` (string)
  - Description: User input query string to search for
  - Example: `"What is humanoid robotics?"`

### Optional Arguments
- `--top_k` (integer)
  - Description: Number of top results to return
  - Default: 5
  - Minimum: 1
  - Maximum: 100
  - Example: `10`

## Exit Codes
- `0`: Success - results retrieved and displayed
- `1`: General error - configuration or runtime error
- `2`: Invalid arguments - incorrect command-line arguments
- `3`: Connection error - unable to connect to external services
- `4`: Authentication error - invalid API credentials

## Environment Variables
- `QDRANT_HOST`: URL for Qdrant service (required)
- `QDRANT_API_KEY`: API key for Qdrant authentication (required)
- `COLLECTION_NAME`: Name of the collection to search (required)
- `COHERE_API_KEY`: API key for Cohere service (required)

## Error Cases and Messages

### Configuration Errors
- Missing environment variable: `Error: Missing required environment variable: {VARIABLE_NAME}`
- Invalid QDRANT_HOST format: `Error: Invalid QDRANT_HOST format: {host}`
- Empty API key: `Error: Invalid {SERVICE}_API_KEY: API key is empty or invalid`
- Collection doesn't exist: `Error: Collection '{collection_name}' does not exist in Qdrant. Available collections: {list}`

### Input Validation Errors
- Empty query: `Error: Query cannot be empty or all whitespace`
- Query too long: `Error: Query is too long (maximum 1000 characters)`
- Invalid top_k: `Error: top_k must be a positive integer between 1 and 100`

### Connection Errors
- Qdrant connection failure: `Error: Failed to connect to Qdrant: {details}`
- Cohere connection failure: `Error: Failed to connect to Cohere: {details}`

### Runtime Errors
- General failures will show: `Error: {specific_error_message}`

## Output Format
```
[1] Score: 0.84
    Source: chapter_3.md
    Chunk: 12
    Text: Humanoid robots use vision and tactile sensors...

[2] Score: 0.78
    Source: chapter_5.pdf
    Chunk: 7
    Text: Advanced locomotion algorithms...
```

## Dependencies
- qdrant-client
- cohere
- python-dotenv

## Performance
- The tool is designed to return results within 5 seconds
- Includes retry logic with exponential backoff for transient failures
- Comprehensive logging for monitoring and debugging