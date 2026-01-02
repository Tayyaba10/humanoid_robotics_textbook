from typing import Optional
from pydantic import BaseModel, Field
import time

class QdrantConnection(BaseModel):
    """Model representing a Qdrant Cloud connection configuration"""

    host: str = Field(..., description="Qdrant Cloud host URL")
    api_key: str = Field(..., description="API key for authentication")
    collection_name: str = Field(..., description="Name of the target collection")
    connection_timeout: int = Field(default=30, description="Connection timeout in seconds")
    status: str = Field(default="disconnected", description="Current connection status")
    last_connected: Optional[float] = Field(default=None, description="Timestamp of last connection")

    def is_connected(self) -> bool:
        """Check if the connection status is active"""
        return self.status == "connected"

    def update_status(self, status: str):
        """Update the connection status"""
        self.status = status
        if status == "connected":
            self.last_connected = time.time()

    class Config:
        arbitrary_types_allowed = True