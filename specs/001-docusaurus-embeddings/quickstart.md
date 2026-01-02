# Quickstart Guide: Docusaurus Embeddings for Humanoid Robotics Textbook

## Overview
This guide provides step-by-step instructions to set up and run the Docusaurus embeddings pipeline that crawls the humanoid robotics textbook website, generates embeddings, and stores them in Qdrant Cloud.

## Prerequisites
- Python 3.8 or higher
- UV package manager
- Access to Cohere API (API key)
- Qdrant Cloud account and cluster

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
# Create backend directory
mkdir backend
cd backend
```

### 2. Set up Python Environment with UV
```bash
# Initialize a new Python project
uv init
# Or if starting fresh in backend directory
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv
```

### 4. Environment Configuration
Create a `.env` file in the backend directory:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
BASE_URL=https://tayyaba10.github.io/humanoid_robotics_textbook/
```

## Running the Pipeline

### 1. Create main.py
Create the main.py file with all required functions as specified in the API contracts.

### 2. Execute the Pipeline
```bash
cd backend
python main.py
```

## Expected Output
- All pages from the humanoid robotics textbook will be crawled
- Content will be extracted, chunked, and embedded
- Chunks will be stored in the `rag_embeddings` collection in Qdrant Cloud
- Progress will be logged to the console

## Troubleshooting

### Common Issues
1. **API Key Errors**: Verify your Cohere and Qdrant API keys are correct
2. **Connection Issues**: Check that your Qdrant URL is accessible
3. **Rate Limits**: The pipeline implements respectful crawling; if you encounter rate limits, consider adding more delays

### Logging
- Progress and errors are logged to the console
- For detailed debugging, add more logging statements to the main.py file

## Next Steps
1. Verify that embeddings are stored correctly in Qdrant Cloud
2. Test similarity search queries against your vector database
3. Integrate with a search interface or RAG application