from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time

class ContentChunk(BaseModel):
    """Model representing a segment of book content retrieved from the Qdrant vector database"""

    id: str = Field(..., description="Unique identifier for the content chunk")
    content: str = Field(..., description="The text content of the chunk")
    metadata: Dict[str, Any] = Field(..., description="Source information including URL, section, and heading")
    embedding: Optional[List[float]] = Field(default=None, description="The vector representation of the content")
    similarity_score: float = Field(..., description="The similarity score from the search operation")
    retrieved_at: float = Field(default_factory=time.time, description="Timestamp when the chunk was retrieved")

    def has_complete_metadata(self) -> bool:
        """Check if the metadata contains the required fields"""
        required_fields = ['url', 'section', 'heading']
        return all(field in self.metadata for field in required_fields)

    def get_metadata_field(self, field: str) -> Any:
        """Get a specific metadata field"""
        return self.metadata.get(field)

    def validate_metadata(self) -> bool:
        """Validate that all required metadata fields are present and not empty"""
        if not self.has_complete_metadata():
            return False
        # Check that required fields are not empty
        for field in ['url', 'section', 'heading']:
            if not self.metadata.get(field):
                return False
        return True

    class Config:
        arbitrary_types_allowed = True