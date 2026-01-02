import logging
from typing import List
from src.lib.embedding_utils import create_embedding, create_embeddings
from backend.src.config import Config

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service to handle text embedding operations using Cohere API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        # Store the API key in the environment for the utility functions
        if not Config.COHERE_API_KEY:
            # We'll use the config directly in the utility functions
            pass

    @classmethod
    def from_config(cls):
        """Create an EmbeddingService instance from configuration"""
        config = Config()
        if not config.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY is not set in configuration")

        return cls(api_key=config.COHERE_API_KEY)

    @classmethod
    def from_env(cls):
        """Create an EmbeddingService instance from environment variables"""
        config = Config()
        if not config.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY is not set in environment")

        return cls(api_key=config.COHERE_API_KEY)

    def create_embedding(self, text: str) -> List[float]:
        """
        Create an embedding vector for the given text

        Args:
            text: The text to convert to an embedding vector

        Returns:
            A list of floats representing the embedding vector
        """
        try:
            logger.info(f"Creating embedding for text: {text[:50]}...")
            embedding = create_embedding(text)
            logger.info(f"Successfully created embedding with {len(embedding)} dimensions")
            return embedding
        except Exception as e:
            logger.error(f"Failed to create embedding for text: {str(e)}")
            raise

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embedding vectors for multiple texts

        Args:
            texts: A list of texts to convert to embedding vectors

        Returns:
            A list of embedding vectors (each vector is a list of floats)
        """
        if not texts:
            logger.warning("Empty text list provided for embedding")
            return []

        try:
            logger.info(f"Creating embeddings for {len(texts)} texts")
            embeddings = create_embeddings(texts)
            logger.info(f"Successfully created {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Failed to create embeddings: {str(e)}")
            raise

    def validate_embedding_dimensions(self, embedding: List[float], expected_dimension: int = None) -> bool:
        """
        Validate that the embedding has the correct dimensions

        Args:
            embedding: The embedding vector to validate
            expected_dimension: The expected dimension size (if None, just checks for valid vector)

        Returns:
            True if the embedding has valid dimensions, False otherwise
        """
        if not embedding:
            logger.error("Empty embedding provided for validation")
            return False

        if not all(isinstance(val, (int, float)) for val in embedding):
            logger.error("Embedding contains non-numeric values")
            return False

        if expected_dimension and len(embedding) != expected_dimension:
            logger.error(f"Embedding dimension mismatch: expected {expected_dimension}, got {len(embedding)}")
            return False

        logger.debug(f"Embedding validation passed: {len(embedding)} dimensions")
        return True

    def get_embedding_model_info(self) -> dict:
        """
        Get information about the embedding model being used

        Returns:
            Dictionary with model information
        """
        return {
            "model": "embed-english-v3.0",
            "input_type": "search_query",
            "dimensions": 1024  # Cohere's English v3 model typically has 1024 dimensions
        }