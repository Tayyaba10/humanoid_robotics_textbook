import logging
import time
from typing import List, Dict, Any, Optional
from backend.src.models.content_chunk import ContentChunk
from backend.src.models.query import Query
from backend.src.services.retrieval_service import RetrievalService

logger = logging.getLogger(__name__)

class ConsistencyResult:
    """Class to represent consistency validation results"""
    def __init__(self, consistency_score: float, is_deterministic: bool, issues: List[Dict[str, Any]] = None):
        self.consistency_score = consistency_score  # Percentage of consistent results (0-100)
        self.is_deterministic = is_deterministic  # Whether results are deterministic
        self.issues = issues or []  # List of consistency issues found
        self.validation_timestamp = time.time()  # Timestamp of validation

    def is_consistent(self) -> bool:
        """Check if the results meet consistency thresholds"""
        return self.consistency_score >= 95.0 and self.is_deterministic

    def to_dict(self) -> Dict[str, Any]:
        """Convert the consistency result to a dictionary"""
        return {
            "consistency_score": self.consistency_score,
            "is_deterministic": self.is_deterministic,
            "issues": self.issues,
            "validation_timestamp": self.validation_timestamp
        }

class ConsistencyService:
    """Service to validate the consistency of retrieval results across multiple queries and sessions"""

    def __init__(self, retrieval_service: RetrievalService):
        self.retrieval_service = retrieval_service
        self._session_cache = {}  # Cache for session-based consistency tracking

    def validate_consistency(self, query_text: str, iterations: int = 5, top_k: int = 5) -> ConsistencyResult:
        """
        Validate consistency by running the same query multiple times and comparing results

        Args:
            query_text: The query text to test for consistency
            iterations: Number of times to run the query (default: 5)
            top_k: Number of results to return (default: 5)

        Returns:
            ConsistencyResult object with validation metrics
        """
        logger.info(f"Validating consistency for query: '{query_text[:50]}...' with {iterations} iterations")

        results = []
        errors = 0

        for i in range(iterations):
            try:
                iteration_results = self.retrieval_service.search(query_text, top_k=top_k)
                results.append(iteration_results)
                logger.debug(f"Iteration {i+1}: Retrieved {len(iteration_results)} results")
            except Exception as e:
                logger.error(f"Iteration {i+1} failed: {str(e)}")
                errors += 1

        if errors == iterations:
            logger.error("All iterations failed, cannot validate consistency")
            return ConsistencyResult(
                consistency_score=0.0,
                is_deterministic=False,
                issues=[{"type": "all_iterations_failed", "message": "All query iterations failed"}]
            )

        # Calculate consistency metrics
        consistency_score = self._calculate_consistency_score(results)
        is_deterministic = self._check_deterministic_results(results)

        # Collect issues if any
        issues = self._collect_consistency_issues(results)

        logger.info(f"Consistency validation completed: {consistency_score}% consistent, deterministic: {is_deterministic}")
        return ConsistencyResult(
            consistency_score=consistency_score,
            is_deterministic=is_deterministic,
            issues=issues
        )

    def _calculate_consistency_score(self, results: List[List[ContentChunk]]) -> float:
        """
        Calculate the consistency score based on result similarity

        Args:
            results: List of result lists from multiple query iterations

        Returns:
            Consistency score as a percentage (0-100)
        """
        if len(results) < 2:
            return 100.0  # Single result is perfectly consistent

        # Compare the first result with all others
        first_result = results[0]
        consistent_comparisons = 0
        total_comparisons = 0

        for i in range(1, len(results)):
            comparison_result = self._compare_results(first_result, results[i])
            if comparison_result >= 0.8:  # 80% similarity threshold
                consistent_comparisons += 1
            total_comparisons += 1

        if total_comparisons == 0:
            return 100.0

        consistency_percentage = (consistent_comparisons / total_comparisons) * 100
        return consistency_percentage

    def _compare_results(self, results1: List[ContentChunk], results2: List[ContentChunk]) -> float:
        """
        Compare two sets of results to determine similarity

        Args:
            results1: First set of results
            results2: Second set of results

        Returns:
            Similarity score between 0 and 1
        """
        if len(results1) == 0 and len(results2) == 0:
            return 1.0
        if len(results1) == 0 or len(results2) == 0:
            return 0.0

        # Calculate similarity based on overlapping content IDs and scores
        ids1 = {chunk.id for chunk in results1}
        ids2 = {chunk.id for chunk in results2}

        intersection = ids1.intersection(ids2)
        union = ids1.union(ids2)

        # Jaccard similarity coefficient
        if len(union) == 0:
            return 1.0

        id_similarity = len(intersection) / len(union)

        # Also consider score similarity for overlapping chunks
        score_similarity = 0.0
        matching_chunks = 0

        for chunk1 in results1:
            for chunk2 in results2:
                if chunk1.id == chunk2.id:
                    # Compare similarity scores
                    score_diff = abs(chunk1.similarity_score - chunk2.similarity_score)
                    score_similarity += max(0, 1 - score_diff)  # Normalize to 0-1 range
                    matching_chunks += 1
                    break

        if matching_chunks > 0:
            score_similarity /= matching_chunks
        else:
            score_similarity = 1.0  # If no matching chunks, don't penalize score similarity

        # Weight ID similarity higher than score similarity
        overall_similarity = 0.7 * id_similarity + 0.3 * score_similarity
        return overall_similarity

    def _check_deterministic_results(self, results: List[List[ContentChunk]]) -> bool:
        """
        Check if the results are deterministic (same order and content across queries)

        Args:
            results: List of result lists from multiple query iterations

        Returns:
            True if results are deterministic, False otherwise
        """
        if len(results) < 2:
            return True  # Single result is deterministic by definition

        first_result = results[0]

        for result in results[1:]:
            if len(first_result) != len(result):
                logger.warning("Results have different lengths across iterations")
                return False

            for i, (chunk1, chunk2) in enumerate(zip(first_result, result)):
                if chunk1.id != chunk2.id:
                    logger.warning(f"Chunk ID mismatch at position {i}: {chunk1.id} != {chunk2.id}")
                    return False

                # Check if similarity scores are reasonably close (allowing for small variations)
                score_diff = abs(chunk1.similarity_score - chunk2.similarity_score)
                if score_diff > 0.01:  # Allow small variations
                    logger.warning(f"Score difference too large at position {i}: {score_diff}")
                    return False

        logger.info("Results are deterministic across all iterations")
        return True

    def _collect_consistency_issues(self, results: List[List[ContentChunk]]) -> List[Dict[str, Any]]:
        """
        Collect any consistency issues found in the results

        Args:
            results: List of result lists from multiple query iterations

        Returns:
            List of consistency issues found
        """
        issues = []

        # Check for varying result counts
        result_counts = [len(result) for result in results]
        if len(set(result_counts)) > 1:
            issues.append({
                "type": "inconsistent_result_count",
                "message": f"Result counts vary across iterations: {result_counts}",
                "counts": result_counts
            })

        # Check for different top results
        if results:
            top_chunks_per_iteration = [result[0].id if result else None for result in results]
            unique_top_chunks = set(top_chunks_per_iteration)
            if len(unique_top_chunks) > 1:
                issues.append({
                    "type": "inconsistent_top_result",
                    "message": f"Top result varies across iterations: {top_chunks_per_iteration}",
                    "top_chunks": top_chunks_per_iteration
                })

        return issues

    def add_result_caching_mechanism(self) -> None:
        """
        Add a result caching mechanism for consistency validation
        """
        logger.info("Initializing result caching mechanism for consistency validation")
        # This would implement caching logic to store and compare results
        # across different sessions and queries
        pass

    def validate_session_consistency(self, session_id: str, query_text: str, top_k: int = 5) -> Optional[ConsistencyResult]:
        """
        Validate consistency for a specific session by comparing with previous results

        Args:
            session_id: The session identifier
            query_text: The query text to validate
            top_k: Number of results to return

        Returns:
            ConsistencyResult if previous results exist, None otherwise
        """
        if session_id not in self._session_cache:
            # Store the first result for this session
            try:
                initial_results = self.retrieval_service.search(query_text, top_k=top_k)
                self._session_cache[session_id] = {
                    "query": query_text,
                    "results": initial_results,
                    "timestamp": time.time()
                }
                logger.info(f"Stored initial results for session {session_id}")
                return None
            except Exception as e:
                logger.error(f"Failed to store initial results for session {session_id}: {str(e)}")
                return None

        # Compare with previous results
        previous_data = self._session_cache[session_id]
        if previous_data["query"] != query_text:
            logger.warning(f"Query changed for session {session_id}, updating cache")
            try:
                new_results = self.retrieval_service.search(query_text, top_k=top_k)
                self._session_cache[session_id] = {
                    "query": query_text,
                    "results": new_results,
                    "timestamp": time.time()
                }
                return None
            except Exception as e:
                logger.error(f"Failed to update cache for session {session_id}: {str(e)}")
                return None

        # Run the query again and compare
        try:
            current_results = self.retrieval_service.search(query_text, top_k=top_k)
            comparison_score = self._compare_results(previous_data["results"], current_results)
            is_deterministic = self._check_deterministic_results([previous_data["results"], current_results])

            logger.info(f"Session {session_id} consistency: {comparison_score * 100:.2f}%")
            return ConsistencyResult(
                consistency_score=comparison_score * 100,
                is_deterministic=is_deterministic,
                issues=self._collect_consistency_issues([previous_data["results"], current_results])
            )
        except Exception as e:
            logger.error(f"Failed to validate session consistency for {session_id}: {str(e)}")
            return None