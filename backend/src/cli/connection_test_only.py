#!/usr/bin/env python3
"""
Test just the connection to Qdrant without search functionality
"""
import os
import logging
from qdrant_client import QdrantClient

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_connection_only():
    # Read environment variables
    qdrant_host = os.getenv('QDRANT_HOST')
    qdrant_api_key = os.getenv('QDRANT_API_KEY')
    collection_name = os.getenv('COLLECTION_NAME')

    if not all([qdrant_host, qdrant_api_key, collection_name]):
        print("ERROR: Missing required environment variables")
        return False

    print(f"Testing connection to Qdrant at: {qdrant_host}")
    print(f"Target collection: {collection_name}")

    try:
        # Initialize client
        client = QdrantClient(
            url=qdrant_host,
            api_key=qdrant_api_key,
            timeout=10
        )

        # Test basic connection by getting collections
        collections = client.get_collections()
        available_collections = [collection.name for collection in collections.collections]
        print(f"✓ Successfully connected to Qdrant")
        print(f"✓ Available collections: {available_collections}")

        # Check if our collection exists
        if collection_name in available_collections:
            print(f"✓ Collection '{collection_name}' exists")

            # Test getting collection info
            collection_info = client.get_collection(collection_name)
            print(f"✓ Collection info retrieved - points count: {collection_info.points_count}")

            # Check what search-related methods are available
            methods = [method for method in dir(client) if 'search' in method.lower() and not method.startswith('_')]
            print(f"✓ Available search methods: {methods}")

            return True
        else:
            print(f"✗ Collection '{collection_name}' not found in available collections")
            return False

    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_connection_only()
    if success:
        print("\n✓ Connection test successful!")
    else:
        print("\n✗ Connection test failed!")