from fastapi import APIRouter, HTTPException, Query
from typing import List
import logging

from src.services.retrieval_service import RetrievalService
from src.services.validation_service import ValidationService, ValidationResult
from src.models.content_chunk import ContentChunk
from src.lib.timing_utils import measure_execution_time, TimingResult
from src.api.models.request_models import RetrieveRequest, RetrieveResponse, ValidationRequest, ValidationResultResponse, CollectionInfoResponse, HealthResponse
from src.models.query import Query as QueryModel

# Create router
router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)

@router.post("/retrieve",
             summary="Retrieve semantically similar content chunks",
             description="Perform semantic similarity search against Qdrant Cloud collection",
             response_model=RetrieveResponse)
async def retrieve_content(
    request: RetrieveRequest
):
    """
    Retrieve semantically similar content chunks based on the provided query.

    Args:
        request: RetrieveRequest object containing query and top_k parameters

    Returns:
        RetrieveResponse: Object containing the search results and metadata

    Raises:
        HTTPException: If there are issues with the query or search process
    """
    try:
        logger.info(f"Processing retrieval request for query: '{request.query[:50]}...' with top_k={request.top_k}")

        # Validate query
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Create retrieval service instance
        retrieval_service = RetrievalService.from_env()

        # Time the retrieval operation
        timing_result: TimingResult = measure_execution_time(
            retrieval_service.search_with_validation,
            request.query,
            request.top_k
        )

        if not timing_result.is_success():
            logger.error(f"Retrieval failed: {timing_result.error}")
            raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(timing_result.error)}")

        results: List[ContentChunk] = timing_result.result

        logger.info(f"Retrieved {len(results)} content chunks in {timing_result.execution_time_ms:.2f} ms")

        # Prepare response
        response = RetrieveResponse(
            results=results,
            execution_time_ms=timing_result.execution_time_ms,
            query_vector=None,  # We could include the query vector if needed
            total_chunks_found=len(results)
        )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error during retrieval: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/validate",
             summary="Validate retrieval results",
             description="Validate the quality of retrieval results for metadata accuracy and content relevance",
             response_model=ValidationResultResponse)
async def validate_retrieval(request: ValidationRequest):
    """
    Validate retrieval results for metadata accuracy and content relevance.

    Args:
        request: ValidationRequest object containing query and top_k parameters

    Returns:
        ValidationResultResponse: Object containing validation metrics
    """
    try:
        logger.info(f"Validating retrieval results for query: '{request.query[:50]}...'")

        # Validate query
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Create services
        retrieval_service = RetrievalService.from_env()
        validation_service = ValidationService()

        # Perform retrieval
        chunks = retrieval_service.search_with_validation(request.query, request.top_k)

        # Perform validation
        query_model = QueryModel(text=request.query)
        validation_result = validation_service.validate_retrieval_results(query_model, chunks)

        logger.info(f"Validation completed: metadata_accuracy={validation_result.metadata_accuracy}%, content_relevance={validation_result.content_relevance}%")

        # Convert to response model
        response = ValidationResultResponse(
            metadata_accuracy=validation_result.metadata_accuracy,
            content_relevance=validation_result.content_relevance,
            issues=validation_result.issues,
            validation_timestamp=validation_result.validation_timestamp,
            is_valid=validation_result.is_valid()
        )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@router.get("/collection-info",
            summary="Get collection information",
            description="Retrieve information about the Qdrant collection being searched",
            response_model=CollectionInfoResponse)
async def get_collection_info():
    """
    Get information about the collection being searched.

    Returns:
        CollectionInfoResponse with collection information
    """
    try:
        logger.info("Retrieving collection information")

        retrieval_service = RetrievalService.from_env()
        collection_info = retrieval_service.get_collection_info()

        logger.info(f"Retrieved collection info for '{collection_info['collection_name']}'")

        response = CollectionInfoResponse(
            name=collection_info['name'],
            vectors_count=collection_info['vectors_count'],
            indexed_vectors_count=collection_info['indexed_vectors_count'],
            collection_name=collection_info['collection_name']
        )

        return response

    except Exception as e:
        logger.error(f"Failed to get collection info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get collection info: {str(e)}")

# Health check for the retrieval endpoint
@router.get("/health",
            summary="Health check for retrieval service",
            description="Check if the retrieval service is properly connected to Qdrant",
            response_model=HealthResponse)
async def retrieval_health():
    """
    Health check for the retrieval service.

    Returns:
        HealthResponse with health status of the retrieval service
    """
    try:
        logger.info("Checking retrieval service health")

        retrieval_service = RetrievalService.from_env()
        collection_info = retrieval_service.get_collection_info()

        response = HealthResponse(
            status="healthy",
            collection_name=collection_info['collection_name'],
            vectors_count=collection_info['vectors_count'],
            timestamp=__import__('time').time()
        )

        logger.info("Retrieval service health check passed")

        return response

    except Exception as e:
        logger.error(f"Retrieval service health check failed: {str(e)}")
        response = HealthResponse(
            status="unhealthy",
            error=str(e),
            timestamp=__import__('time').time()
        )
        return response