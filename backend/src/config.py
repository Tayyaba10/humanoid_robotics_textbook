import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class to manage application settings"""

    # Qdrant Configuration
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "default_collection")
    CONNECTION_TIMEOUT: int = int(os.getenv("CONNECTION_TIMEOUT", "30"))

    # Cohere Configuration
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration values are present"""
        required_fields = [
            cls.QDRANT_HOST,
            cls.QDRANT_API_KEY,
            cls.COLLECTION_NAME,
            cls.COHERE_API_KEY
        ]
        return all(field != "" for field in required_fields)

    @classmethod
    def get_missing_fields(cls) -> list:
        """Get list of missing required configuration fields"""
        missing = []
        if not cls.QDRANT_HOST:
            missing.append("QDRANT_HOST")
        if not cls.QDRANT_API_KEY:
            missing.append("QDRANT_API_KEY")
        if not cls.COLLECTION_NAME:
            missing.append("COLLECTION_NAME")
        if not cls.COHERE_API_KEY:
            missing.append("COHERE_API_KEY")
        return missing