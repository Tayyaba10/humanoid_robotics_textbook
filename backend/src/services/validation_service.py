import logging
from typing import List, Dict, Any
from backend.src.models.content_chunk import ContentChunk
from backend.src.models.query import Query
from backend.src.services.retrieval_service import RetrievalService

logger = logging.getLogger(__name__)

class ValidationResult:
    """Model representing the validation results for retrieved content chunks"""

    def __init__(self, metadata_accuracy: float, content_relevance: float, issues: List[Dict[str, Any]] = None):
        self.metadata_accuracy = metadata_accuracy  # Percentage of accurate metadata fields (0-100)
        self.content_relevance = content_relevance  # Relevance score of content to query (0-100)
        self.issues = issues or []  # Array of validation issues found
        self.validation_timestamp = __import__('time').time()  # ISO 8601 timestamp of validation

    def is_valid(self) -> bool:
        """Check if the validation result meets minimum thresholds"""
        return self.metadata_accuracy >= 95.0 and self.content_relevance >= 80.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert the validation result to a dictionary"""
        return {
            "metadata_accuracy": self.metadata_accuracy,
            "content_relevance": self.content_relevance,
            "issues": self.issues,
            "validation_timestamp": self.validation_timestamp
        }

class ValidationService:
    """Service to validate the accuracy and relevance of retrieved content chunks"""

    def __init__(self):
        pass

    def validate_retrieval_results(self, query: Query, chunks: List[ContentChunk]) -> ValidationResult:
        """
        Validate the retrieval results for metadata accuracy and content relevance

        Args:
            query: The original query used for retrieval
            chunks: The list of content chunks retrieved

        Returns:
            ValidationResult object containing validation metrics
        """
        if not chunks:
            logger.warning("No chunks provided for validation")
            return ValidationResult(
                metadata_accuracy=0.0,
                content_relevance=0.0,
                issues=[{"type": "empty_results", "message": "No chunks returned from retrieval"}]
            )

        # Validate metadata accuracy
        metadata_accuracy = self._validate_metadata_accuracy(chunks)
        logger.info(f"Metadata accuracy: {metadata_accuracy}%")

        # Validate content relevance (basic approach - can be enhanced)
        content_relevance = self._validate_content_relevance(query, chunks)
        logger.info(f"Content relevance: {content_relevance}%")

        # Collect any issues found during validation
        issues = self._collect_validation_issues(chunks)

        return ValidationResult(
            metadata_accuracy=metadata_accuracy,
            content_relevance=content_relevance,
            issues=issues
        )

    def _validate_metadata_accuracy(self, chunks: List[ContentChunk]) -> float:
        """
        Validate the accuracy of metadata in the retrieved chunks

        Args:
            chunks: The list of content chunks to validate

        Returns:
            Percentage of chunks with accurate metadata (0-100)
        """
        if not chunks:
            return 0.0

        valid_chunks = 0
        for chunk in chunks:
            if chunk.validate_metadata():
                valid_chunks += 1

        accuracy = (valid_chunks / len(chunks)) * 100
        return accuracy

    def _validate_content_relevance(self, query: Query, chunks: List[ContentChunk]) -> float:
        """
        Validate the relevance of content to the original query (basic implementation)

        Args:
            query: The original query
            chunks: The list of content chunks to validate

        Returns:
            Estimated relevance percentage (0-100)
        """
        if not chunks or not query.text:
            return 0.0

        # Basic relevance check: look for query terms in content
        query_terms = set(query.text.lower().split())

        total_relevance_score = 0
        for chunk in chunks:
            chunk_terms = set(chunk.content.lower().split())
            # Calculate overlap between query terms and chunk terms
            overlap = len(query_terms.intersection(chunk_terms))
            max_possible = min(len(query_terms), len(chunk_terms))

            if max_possible > 0:
                term_relevance = (overlap / max_possible) * 100
            else:
                term_relevance = 0

            # Also factor in the similarity score from Qdrant
            score_based_relevance = chunk.similarity_score * 100

            # Average the two relevance measures
            chunk_relevance = (term_relevance + score_based_relevance) / 2
            total_relevance_score += chunk_relevance

        # Average relevance across all chunks
        avg_relevance = total_relevance_score / len(chunks)

        # Cap the relevance at 100%
        return min(100.0, avg_relevance)

    def _collect_validation_issues(self, chunks: List[ContentChunk]) -> List[Dict[str, Any]]:
        """
        Collect any validation issues found in the chunks

        Args:
            chunks: The list of content chunks to check

        Returns:
            List of validation issues found
        """
        issues = []

        for i, chunk in enumerate(chunks):
            if not chunk.validate_metadata():
                issues.append({
                    "type": "metadata_incomplete",
                    "chunk_id": chunk.id,
                    "message": f"Chunk {i} has incomplete metadata"
                })

            if not chunk.content.strip():
                issues.append({
                    "type": "empty_content",
                    "chunk_id": chunk.id,
                    "message": f"Chunk {i} has empty content"
                })

            if chunk.similarity_score < 0.1:  # Very low similarity
                issues.append({
                    "type": "low_similarity",
                    "chunk_id": chunk.id,
                    "message": f"Chunk {i} has very low similarity score: {chunk.similarity_score}",
                    "score": chunk.similarity_score
                })

        return issues

    def validate_metadata_completeness(self, chunks: List[ContentChunk]) -> Dict[str, Any]:
        """
        Validate the completeness of metadata across all chunks

        Args:
            chunks: The list of content chunks to validate

        Returns:
            Dictionary with metadata validation metrics
        """
        if not chunks:
            return {
                "total_chunks": 0,
                "chunks_with_complete_metadata": 0,
                "completeness_percentage": 0.0,
                "missing_fields": {}
            }

        complete_chunks = 0
        missing_fields = {}

        for chunk in chunks:
            if chunk.validate_metadata():
                complete_chunks += 1
            else:
                # Count which fields are missing
                required_fields = ['url', 'section', 'heading']
                for field in required_fields:
                    if not chunk.metadata.get(field):
                        missing_fields[field] = missing_fields.get(field, 0) + 1

        completeness_percentage = (complete_chunks / len(chunks)) * 100

        return {
            "total_chunks": len(chunks),
            "chunks_with_complete_metadata": complete_chunks,
            "completeness_percentage": completeness_percentage,
            "missing_fields": missing_fields
        }

    def validate_result_ordering(self, chunks: List[ContentChunk]) -> bool:
        """
        Validate that the chunks are properly ordered by similarity score

        Args:
            chunks: The list of content chunks to validate

        Returns:
            True if chunks are properly ordered, False otherwise
        """
        if len(chunks) <= 1:
            return True

        # Check if chunks are ordered by similarity score (descending)
        for i in range(len(chunks) - 1):
            if chunks[i].similarity_score < chunks[i + 1].similarity_score:
                logger.warning(f"Chunks not properly ordered: {chunks[i].similarity_score} < {chunks[i + 1].similarity_score}")
                return False

        logger.info("Chunks are properly ordered by similarity score (descending)")
        return True