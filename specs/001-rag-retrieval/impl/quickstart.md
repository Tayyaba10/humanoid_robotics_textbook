# Quickstart Guide: RAG Retrieval CLI Tool

**Feature**: 001-rag-retrieval
**Created**: 2025-12-26
**Status**: Draft

## Prerequisites

1. Python 3.11 or higher
2. Access to Qdrant Cloud instance with a populated collection
3. Cohere API key
4. Required Python packages installed:
   - qdrant-client
   - cohere
   - python-dotenv

## Installation

1. Install required packages:
```bash
pip install qdrant-client cohere python-dotenv
```

2. Ensure your Qdrant collection is populated with embeddings and metadata.

## Configuration

Set the required environment variables:

```bash
export QDRANT_HOST="https://your-cluster.qdrant.tech:6333"
export QDRANT_API_KEY="your-api-key-here"
export COLLECTION_NAME="your-collection-name"
export COHERE_API_KEY="your-cohere-api-key-here"
```

Alternatively, create a `.env` file in your working directory:

```env
QDRANT_HOST=https://your-cluster.qdrant.tech:6333
QDRANT_API_KEY=your-api-key-here
COLLECTION_NAME=your-collection-name
COHERE_API_KEY=your-cohere-api-key-here
```

## Basic Usage

Run a simple query:

```bash
python -m backend.src.cli.retrieve --query "What is humanoid robotics?" --top_k 5
```

## Common Examples

### Retrieve top 3 results:
```bash
python -m backend.src.cli.retrieve --query "locomotion algorithms" --top_k 3
```

### Default result count (5):
```bash
python -m backend.src.cli.retrieve --query "sensor fusion techniques"
```

## Troubleshooting

### Connection Issues
- Verify QDRANT_HOST is correct and accessible
- Check that QDRANT_API_KEY is valid
- Ensure the collection name exists

### Authentication Issues
- Confirm API keys are correct
- Check that keys have appropriate permissions

### Empty Results
- Verify the collection contains relevant data
- Try different query terms
- Check that the collection name is correct

## Expected Output Format

Results will be displayed as:

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