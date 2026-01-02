from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.api.endpoints import retrieval
from src.config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="Qdrant RAG Retrieval Service",
    description="API for retrieving semantically similar content chunks from Qdrant Cloud",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(retrieval.router, prefix="/api", tags=["retrieval"])

@app.get("/")
def read_root():
    """Root endpoint to verify API is running"""
    return {
        "message": "Qdrant RAG Retrieval Service",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    # Validate configuration
    config = Config()
    config_issues = config.get_missing_fields()

    if config_issues:
        raise HTTPException(
            status_code=500,
            detail=f"Configuration issues: {', '.join(config_issues)}"
        )

    return {
        "status": "healthy",
        "timestamp": __import__('time').time(),
        "config_valid": config.validate()
    }

# Error handlers
@app.exception_handler(500)
async def internal_exception_handler(request, exc):
    logger.error(f"Internal server error: {str(exc)}")
    return {"error": "Internal server error", "detail": str(exc)}

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Not found", "detail": str(exc)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)