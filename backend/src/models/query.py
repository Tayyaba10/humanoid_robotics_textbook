from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import time

class Query(BaseModel):
    """Model representing a natural language query for semantic similarity search"""

    text: str = Field(..., description="The natural language query text")
    vector: Optional[List[float]] = Field(default=None, description="The embedding vector representation of the query text")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional query parameters and context information")
    created_at: float = Field(default_factory=time.time, description="Timestamp when the query was created")
    processed_at: Optional[float] = Field(default=None, description="Timestamp when the query was processed")

    def is_vectorized(self) -> bool:
        """Check if the query has been converted to an embedding vector"""
        return self.vector is not None and len(self.vector) > 0

    def vectorize(self, vector: List[float]):
        """Set the embedding vector for the query"""
        self.vector = vector
        self.processed_at = time.time()

    class Config:
        arbitrary_types_allowed = True