from pydantic import BaseModel, Field
from typing import List, Optional
from src.models.content_chunk import ContentChunk

class RetrieveRequest(BaseModel):
    """Request model for the retrieve endpoint"""
    query: str = Field(
        ...,
        description="Natural language query to search for",
        min_length=1,
        max_length=1000
    )
    top_k: int = Field(
        5,
        description="Number of results to return",
        ge=1,
        le=20
    )
    validate_results: bool = Field(
        False,
        description="Whether to validate the results for metadata accuracy and content relevance"
    )

class RetrieveResponse(BaseModel):
    """Response model for the retrieve endpoint"""
    results: List[ContentChunk] = Field(..., description="List of retrieved content chunks")
    execution_time_ms: Optional[float] = Field(None, description="Time taken to execute the search in milliseconds")
    query_vector: Optional[List[float]] = Field(None, description="The embedding vector used for the search")
    total_chunks_found: int = Field(..., description="Total number of chunks found before filtering")

    class Config:
        # Allow the model to work with our existing ContentChunk objects
        arbitrary_types_allowed = True

class ValidationRequest(BaseModel):
    """Request model for the validation endpoint"""
    query: str = Field(
        ...,
        description="Original query text",
        min_length=1,
        max_length=1000
    )
    top_k: int = Field(
        5,
        description="Number of results to validate",
        ge=1,
        le=20
    )

class ValidationResultResponse(BaseModel):
    """Response model for validation results"""
    metadata_accuracy: float = Field(..., description="Percentage of accurate metadata fields (0-100)")
    content_relevance: float = Field(..., description="Relevance score of content to query (0-100)")
    issues: List[dict] = Field(..., description="Array of validation issues found")
    validation_timestamp: float = Field(..., description="Timestamp of validation")
    is_valid: bool = Field(..., description="Whether the results meet minimum validation thresholds")

class CollectionInfoResponse(BaseModel):
    """Response model for collection information"""
    name: int = Field(..., description="Size of vectors in the collection")
    vectors_count: int = Field(..., description="Total number of vectors in the collection")
    indexed_vectors_count: int = Field(..., description="Number of indexed vectors")
    collection_name: str = Field(..., description="Name of the collection")

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Health status (healthy/unhealthy)")
    timestamp: float = Field(..., description="Timestamp of the health check")
    collection_name: Optional[str] = Field(None, description="Name of the collection if healthy")
    vectors_count: Optional[int] = Field(None, description="Number of vectors if healthy")
    error: Optional[str] = Field(None, description="Error message if unhealthy")