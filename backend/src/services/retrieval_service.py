import logging
from typing import List, Optional
from qdrant_client.http.models import SearchRequest
from backend.src.services.qdrant_connection import QdrantConnectionService
from backend.src.services.embedding_service import EmbeddingService
from backend.src.models.query import Query
from backend.src.models.content_chunk import ContentChunk

logger = logging.getLogger(__name__)

class RetrievalService:
    """Service to handle semantic similarity searches against Qdrant Cloud"""

    def __init__(self, qdrant_service: QdrantConnectionService, embedding_service: EmbeddingService):
        self.qdrant_service = qdrant_service
        self.embedding_service = embedding_service
        self.client = qdrant_service.get_client()

    @classmethod
    def from_env(cls):
        """Create a RetrievalService instance from environment variables"""
        qdrant_service = QdrantConnectionService.from_env()
        embedding_service = EmbeddingService.from_env()

        # Connect to Qdrant if not already connected
        if not qdrant_service.is_connected():
            connected = qdrant_service.connect()
            if not connected:
                raise Exception("Failed to connect to Qdrant Cloud")

        return cls(qdrant_service=qdrant_service, embedding_service=embedding_service)

    def search(self, query_text: str, top_k: int = 5) -> List[ContentChunk]:
        """
        Perform a semantic similarity search against the Qdrant collection

        Args:
            query_text: The natural language query text
            top_k: Number of results to return (default: 5)

        Returns:
            List of ContentChunk objects containing the most similar content
        """
        try:
            logger.info(f"Starting semantic search for query: '{query_text[:50]}...'")

            # Create a Query object
            query = Query(text=query_text)

            # Generate embedding for the query
            query_embedding = self.embedding_service.create_embedding(query_text)
            query.vectorize(query_embedding)

            logger.info(f"Query vectorized with {len(query_embedding)} dimensions")

            # Perform the search in Qdrant
            client = self.qdrant_service.get_client()
            collection_name = self.qdrant_service.get_collection_name()

            search_result = self.client.query_points(
                collection_name=collection_name,
                vector=query_embedding,
                limit=top_k,
                with_payload=True 
            )

            logger.info(f"Search completed, found {len(search_result)} results")

            # Convert search results to ContentChunk objects
            content_chunks = []
            for point in search_result.points:
                # Extract payload and vector
                payload = point.payload
                vector = point.vector
                score = getattr(point, 'score', None) 

                # Create ContentChunk from search result
                chunk = ContentChunk(
                    id=str(point.id),
                    content=payload.get('content', ''),
                    metadata=payload.get('metadata', {}),
                    embedding=vector,
                    similarity_score=score
                )

                content_chunks.append(chunk)

            logger.info(f"Converted {len(content_chunks)} results to ContentChunk objects")
            return content_chunks

        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise

    def search_with_validation(self, query_text: str, top_k: int = 5) -> List[ContentChunk]:
        """
        Perform a semantic similarity search with additional validation

        Args:
            query_text: The natural language query text
            top_k: Number of results to return (default: 5)

        Returns:
            List of validated ContentChunk objects containing the most similar content
        """
        try:
            logger.info(f"Starting validated semantic search for query: '{query_text[:50]}...'")

            # Perform the basic search
            results = self.search(query_text, top_k)

            # Validate results
            validated_results = []
            for chunk in results:
                if chunk.validate_metadata():
                    validated_results.append(chunk)
                    logger.debug(f"Validated chunk {chunk.id} with score {chunk.similarity_score}")
                else:
                    logger.warning(f"Chunk {chunk.id} has invalid metadata and will be skipped")

            logger.info(f"Validation completed: {len(validated_results)}/{len(results)} results passed validation")
            return validated_results

        except Exception as e:
            logger.error(f"Validated search failed: {str(e)}")
            raise

    def get_collection_info(self) -> dict:
        """
        Get information about the collection being searched

        Returns:
            Dictionary with collection information
        """
        try:
            client = self.qdrant_service.get_client()
            collection_name = self.qdrant_service.get_collection_name()

            collection_info = client.get_collection(collection_name)

            return {
                "name": collection_info.config.params.vectors_config.size,
                "vectors_count": collection_info.points_count,
                "indexed_vectors_count": collection_info.indexed_vectors_count,
                "collection_name": collection_name
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {str(e)}")
            raise

    def validate_query_text(self, query_text: str) -> bool:
        """
        Validate the query text before processing

        Args:
            query_text: The query text to validate

        Returns:
            True if the query is valid, False otherwise
        """
        if not query_text or not query_text.strip():
            logger.error("Query text is empty or contains only whitespace")
            return False

        if len(query_text.strip()) > 10000:  # Arbitrary limit, can be adjusted
            logger.error(f"Query text is too long: {len(query_text)} characters")
            return False

        return True