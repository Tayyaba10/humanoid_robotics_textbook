#!/usr/bin/env python3
"""
Connection validation script for Qdrant RAG Retrieval Pipeline.
This script validates the connection to Qdrant Cloud and tests basic functionality.
"""

import sys
import logging
from src.services.qdrant_connection import QdrantConnectionService

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_connection():
    """
    Validate the Qdrant Cloud connection.

    Returns:
        int: 0 if validation succeeds, 1 if it fails
    """
    print("Qdrant Cloud Connection Validation Script")
    print("=" * 50)

    service = None
    try:
        # Initialize service from environment
        print("1. Initializing Qdrant connection service...")
        service = QdrantConnectionService.from_env()
        print("   ✓ Service initialized from environment variables")

        # Connect to Qdrant
        print("\n2. Attempting connection to Qdrant Cloud...")
        connected = service.connect()
        if connected:
            print("   ✓ Successfully connected to Qdrant Cloud")
        else:
            print("   ✗ Failed to connect to Qdrant Cloud")
            return 1

        # Test the connection
        print("\n3. Testing connection with collection access...")
        test_result = service.test_connection()
        if test_result:
            print("   ✓ Connection test passed - collection is accessible")
        else:
            print("   ✗ Connection test failed - collection not accessible")
            return 1

        # Additional validation: check if we can list collections
        print("\n4. Verifying collection access...")
        client = service.get_client()
        if client:
            collections = client.get_collections()
            collection_names = [col.name for col in collections.collections]
            print(f"   ✓ Available collections: {collection_names}")

            target_collection = service.get_collection_name()
            if target_collection in collection_names:
                print(f"   ✓ Target collection '{target_collection}' exists")
            else:
                print(f"   ✗ Target collection '{target_collection}' not found")
                return 1
        else:
            print("   ✗ Could not get Qdrant client")
            return 1

        print("\n" + "=" * 50)
        print("✓ All connection validations passed!")
        print("✓ Qdrant Cloud connection is ready for RAG retrieval pipeline")
        return 0

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n✗ Configuration error: {e}")
        print("\nPlease ensure all required environment variables are set:")
        print("  - QDRANT_HOST: Your Qdrant Cloud cluster URL")
        print("  - QDRANT_API_KEY: Your Qdrant API key")
        print("  - COLLECTION_NAME: The name of your embeddings collection")
        print("  - COHERE_API_KEY: Your Cohere API key (needed for later operations)")
        return 1

    except Exception as e:
        logger.error(f"Connection validation failed: {e}")
        print(f"\n✗ Connection validation failed: {e}")
        logger.exception("Full traceback:")
        return 1

    finally:
        # Clean up connection
        if service:
            try:
                service.disconnect()
                print("   ✓ Disconnected from Qdrant Cloud")
            except Exception as e:
                logger.warning(f"Error during disconnect: {e}")

def main():
    """Main entry point for the validation script."""
    try:
        result = validate_connection()
        sys.exit(result)
    except KeyboardInterrupt:
        print("\n\nValidation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Critical error in validation script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()