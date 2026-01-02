# Docusaurus Embeddings Backend

This backend system crawls the humanoid robotics textbook website, extracts content, generates embeddings using Cohere, and stores them in Qdrant Cloud for RAG (Retrieval Augmented Generation) applications.

## Features

- Discovers all pages from a Docusaurus website
- Extracts clean text content while preserving context
- Chunks text with appropriate boundaries
- Generates embeddings using Cohere's multilingual model
- Stores embeddings in Qdrant Cloud with metadata

## Prerequisites

- Python 3.8+
- UV package manager (optional but recommended)
- Cohere API key
- Qdrant Cloud account and cluster

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ai-and-robotics
   ```

2. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

3. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or if using UV:
   ```bash
   uv pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   Create a `.env` file in the backend directory:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cluster_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   BASE_URL=https://tayyaba10.github.io/humanoid_robotics_textbook/
   ```

## Usage

Run the complete pipeline:
```bash
cd backend
python main.py
```

The pipeline will:
1. Discover all URLs from the specified Docusaurus site
2. Extract content from each page
3. Chunk the content appropriately
4. Generate embeddings using Cohere
5. Store the embeddings in Qdrant Cloud

## Configuration

- **BASE_URL**: The Docusaurus website to crawl (default: `https://tayyaba10.github.io/humanoid_robotics_textbook/`)
- **COHERE_API_KEY**: Your Cohere API key for embedding generation
- **QDRANT_URL**: Your Qdrant Cloud cluster URL
- **QDRANT_API_KEY**: Your Qdrant Cloud API key

## Architecture

The system consists of these main functions:

- `get_all_urls()`: Discovers all accessible URLs from the Docusaurus site
- `extract_text_from_url()`: Extracts clean text content from a URL
- `chunk_text()`: Splits content into appropriately sized chunks
- `embed()`: Generates embeddings using Cohere's model
- `create_collection()`: Creates a Qdrant collection for storage
- `save_chunk_to_qdrant()`: Stores embeddings with metadata in Qdrant
- `main()`: Orchestrates the complete pipeline

## Output

The system stores content chunks with the following metadata in Qdrant:
- URL source
- Section and heading information
- Content text
- Word and token counts
- Source position in the original document
- Embedding vector

## Troubleshooting

- If you encounter rate limiting, consider adding more delays between requests
- Ensure your Cohere and Qdrant credentials are valid
- Check that the target website allows crawling in its robots.txt