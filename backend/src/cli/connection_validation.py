#!/usr/bin/env python3
"""
Connection validation script for Qdrant Cloud.
This script reads environment variables and validates the connection to Qdrant Cloud.
"""
import os
import sys
import logging
from backend.src.services.qdrant_connection import QdrantConnectionService

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    print("Qdrant Cloud Connection Validation")
    print("=" * 40)

    # Check if environment variables are set
    qdrant_host = os.getenv('QDRANT_HOST')
    qdrant_api_key = os.getenv('QDRANT_API_KEY')
    collection_name = os.getenv('COLLECTION_NAME')

    print(f"Environment Variables Status:")
    print(f"  QDRANT_HOST: {'SET' if qdrant_host else 'NOT SET'}")
    print(f"  QDRANT_API_KEY: {'SET' if qdrant_api_key else 'NOT SET'}")
    print(f"  COLLECTION_NAME: {'SET' if collection_name else 'NOT SET'}")

    if not all([qdrant_host, qdrant_api_key, collection_name]):
        print("\n✗ ERROR: Missing required environment variables")
        print("Please set QDRANT_HOST, QDRANT_API_KEY, and COLLECTION_NAME")
        return 1

    try:
        # Initialize the Qdrant connection service
        print(f"\nInitializing connection to: {qdrant_host}")
        print(f"Target collection: {collection_name}")

        service = QdrantConnectionService(
            host=qdrant_host,
            api_key=qdrant_api_key,
            collection_name=collection_name
        )

        print("✓ Qdrant connection service initialized")

        # Attempt to connect
        print("\nAttempting to connect to Qdrant Cloud...")
        connected = service.connect()

        if connected:
            print("✓ Successfully connected to Qdrant Cloud")

            # Log connection status
            print("\n✓ Connection Status: ACTIVE")

            # Get available collections
            try:
                collections_response = service.client.get_collections()
                available_collections = [collection.name for collection in collections_response.collections]
                print(f"✓ Available Collections: {available_collections}")

                # Log available collections
                logger.info(f"Available collections in Qdrant: {available_collections}")
            except Exception as e:
                print(f"✗ Failed to retrieve collections: {e}")
                return 1

            # Validate the specified collection exists
            print(f"\nValidating collection: {collection_name}")
            if collection_name in available_collections:
                print(f"✓ Collection '{collection_name}' exists and is accessible")

                # Get collection info
                try:
                    collection_info = service.client.get_collection(collection_name)
                    print(f"✓ Collection points count: {collection_info.points_count}")
                    print(f"✓ Collection vectors count: {collection_info.vectors_count}")

                    # Log collection validation result
                    logger.info(f"Collection '{collection_name}' validation successful")
                    logger.info(f"Collection points: {collection_info.points_count}")
                    logger.info(f"Collection vectors: {collection_info.vectors_count}")

                except Exception as e:
                    print(f"✗ Failed to get collection info: {e}")
                    return 1
            else:
                print(f"✗ Collection '{collection_name}' not found in Qdrant")
                print(f"Available collections: {available_collections}")
                return 1

            print("\n" + "=" * 40)
            print("✓ Connection validation completed successfully!")
            print("✓ All checks passed - Qdrant Cloud connection is working properly")

            # Disconnect from Qdrant
            service.disconnect()
            print("✓ Disconnected from Qdrant Cloud")

            return 0
        else:
            print("✗ Failed to connect to Qdrant Cloud")
            print("  Please check your environment variables and network connection")
            return 1

    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("\nPlease ensure all required environment variables are set:")
        print("  - QDRANT_HOST")
        print("  - QDRANT_API_KEY")
        print("  - COLLECTION_NAME")
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        logger.exception("Unexpected error during connection validation")
        return 1

if __name__ == "__main__":
    sys.exit(main())