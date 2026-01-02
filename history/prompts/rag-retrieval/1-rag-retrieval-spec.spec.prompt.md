---
id: 1-rag-retrieval-spec
title: "Create RAG Retrieval CLI Tool Specification"
stage: spec
date: "2025-12-26"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "rag-retrieval"
branch: "001-rag-retrieval"
user: "user"
command: "/sp.specify Create a Python CLI script named `retrieve.py` for the RAG retrieval pipeline..."
labels:
  - "specification"
  - "cli-tool"
  - "rag"
  - "retrieval"
links:
  spec: "specs/001-rag-retrieval/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-rag-retrieval/spec.md"
  - "specs/001-rag-retrieval/checklists/requirements.md"
tests: []
---

## Prompt

```
Create a Python CLI script named `retrieve.py` for the RAG retrieval pipeline with the following specifications:

- **Purpose**: Retrieve top-k relevant embeddings from Qdrant Cloud for a user-provided query and display content + metadata + similarity scores.

- **Environment Variables**: Read the following:
    - QDRANT_HOST
    - QDRANT_API_KEY
    - COLLECTION_NAME
    - COHERE_API_KEY

- **Functionality**:
    1. Connect to Qdrant Cloud using QDRANT_HOST and QDRANT_API_KEY.
    2. Load the specified COLLECTION_NAME and confirm it exists.
    3. Accept CLI arguments:
        - `--query`: User input query string.
        - `--top_k`: Number of top results to return.
    4. Use Cohere embeddings to encode the query.
    5. Perform semantic search in Qdrant collection.
    6. Return and print top-k results with:
        - Content text
        - Source file or document
        - Chunk index
        - Similarity score

- **Error Handling**:
    - Print clear error if connection fails, collection does not exist, or query is empty.
    - Validate top_k is positive integer.

- **Logging**:
    - Log each connection attempt and retrieval request.
    - Print success messages on successful retrieval.

- **Output Format**:
    ```
    [1] Score: 0.84
        Source: chapter_3.md
        Chunk: 12
        Text: Humanoid robots use vision and tactile sensors...
    [2] Score: 0.78
        ...
    ```
- **Usage Example**:
    ```bash
    python -m backend.src.cli.retrieve --query "What is humanoid robotics?" --top_k 5
    ```

- **Bonus (Optional)**: Automatically trim whitespace/quotes from environment variables to prevent invalid URL/port errors.
```

## Response

Created a comprehensive feature specification for the RAG retrieval CLI tool. The specification includes:

1. User scenarios and testing with prioritized user stories
2. Functional requirements covering all core functionality
3. Key entities involved in the system
4. Measurable success criteria

The specification was made technology-agnostic by removing implementation-specific details like "Python", "Qdrant Cloud", and "Cohere", replacing them with more generic terms like "command-line interface tool", "vector database", and "embedding service".

The specification includes:
- User story for querying the RAG system for relevant content
- Error handling for configuration and connection issues
- Input parameter validation
- Edge cases for various failure scenarios
- 11 functional requirements covering connection, search, display, validation, and logging
- 5 measurable success criteria with specific metrics

A quality checklist was also created and validated, confirming that the specification meets all requirements for proceeding to the planning phase.

The specification is now ready for the planning phase (/sp.plan).