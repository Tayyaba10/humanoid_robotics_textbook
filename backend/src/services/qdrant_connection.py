import logging
import time
from typing import Optional
from qdrant_client import QdrantClient
from qdrant_client.http.models import CollectionInfo
from backend.src.models.qdrant_connection import QdrantConnection as QdrantConnectionModel
from backend.src.config import Config

logger = logging.getLogger(__name__)

class QdrantConnectionService:
    """Service to handle Qdrant Cloud connection and operations"""

    def __init__(self, host: str, api_key: str, collection_name: str, connection_timeout: int = 30):
        self.host = host
        self.api_key = api_key
        self.collection_name = collection_name
        self.connection_timeout = connection_timeout
        self.client: Optional[QdrantClient] = None
        self._connected = False

    @classmethod
    def from_config(cls):
        """Create a QdrantConnectionService instance from configuration"""
        config = Config()
        if not config.validate():
            missing_fields = config.get_missing_fields()
            raise ValueError(f"Missing required configuration fields: {', '.join(missing_fields)}")

        return cls(
            host=config.QDRANT_HOST,
            api_key=config.QDRANT_API_KEY,
            collection_name=config.COLLECTION_NAME,
            connection_timeout=config.CONNECTION_TIMEOUT
        )

    @classmethod
    def from_env(cls):
        """Create a QdrantConnectionService instance from environment variables"""
        config = Config()
        if not config.validate():
            missing_fields = config.get_missing_fields()
            raise ValueError(f"Missing required environment variables: {', '.join(missing_fields)}")

        return cls(
            host=config.QDRANT_HOST,
            api_key=config.QDRANT_API_KEY,
            collection_name=config.COLLECTION_NAME,
            connection_timeout=config.CONNECTION_TIMEOUT
        )

    def connect(self) -> bool:
        """Establish connection to Qdrant Cloud"""
        try:
            self.client = QdrantClient(
                url=self.host,
                api_key=self.api_key,
                timeout=self.connection_timeout,
                prefer_grpc=True
            )

            # Test the connection by getting collections
            collections = self.client.get_collections()
            logger.info(f"Successfully connected to Qdrant Cloud. Available collections: {len(collections.collections)}")

            self._connected = True
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant Cloud: {str(e)}")
            self._connected = False
            return False

    def disconnect(self):
        """Disconnect from Qdrant Cloud"""
        if self.client:
            # QdrantClient doesn't have an explicit disconnect method
            # The connection will be closed when the client object is garbage collected
            self.client = None
        self._connected = False
        logger.info("Disconnected from Qdrant Cloud")

    def is_connected(self) -> bool:
        """Check if currently connected to Qdrant Cloud"""
        return self._connected

    def test_connection(self) -> bool:
        """Test the connection by performing a simple operation"""
        if not self.client:
            return False

        try:
            # Try to get collection info to test the connection
            collection_info: CollectionInfo = self.client.get_collection(self.collection_name)
            logger.info(f"Connection test successful. Collection '{self.collection_name}' found with {collection_info.points_count} points")
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False

    def get_client(self) -> Optional[QdrantClient]:
        """Get the Qdrant client instance"""
        if self.client is None:
        # auto-connect if client not yet created
            self.connect()
        return self.client

    def get_collection_name(self) -> str:
        """Get the target collection name"""
        return self.collection_name

    def add_connection_timeout_and_retry_logic(self, max_retries: int = 3) -> bool:
        """Add retry logic for connection with timeout"""
        for attempt in range(max_retries):
            try:
                self.client = QdrantClient(
                    url=self.host,
                    api_key=self.api_key,
                    timeout=self.connection_timeout
                )

                # Test the connection
                collections = self.client.get_collections()
                logger.info(f"Successfully connected to Qdrant Cloud (attempt {attempt + 1}). Available collections: {len(collections.collections)}")

                self._connected = True
                return True
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All {max_retries} connection attempts failed")
                    self._connected = False

        return False