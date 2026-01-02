import sys
import logging
from backend.src.services.qdrant_connection import QdrantConnectionService

# Set up logging for the CLI command
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function to run the connection validation test"""
    print("Qdrant Cloud Connection Validation")
    print("=" * 40)

    try:
        # Create Qdrant connection service from environment
        print("Initializing Qdrant connection service from environment variables...")
        service = QdrantConnectionService.from_env()
        print("✓ Service initialized successfully")

        # Attempt to connect
        print("\nAttempting to connect to Qdrant Cloud...")
        connected = service.connect()

        if connected:
            print("✓ Successfully connected to Qdrant Cloud")

            # Test the connection
            print("\nTesting connection with collection lookup...")
            test_result = service.test_connection()
            if test_result:
                print("✓ Connection test passed - collection found")
            else:
                print("✗ Connection test failed - collection not accessible")
                return 1
        else:
            print("✗ Failed to connect to Qdrant Cloud")
            print("  Please check your environment variables and network connection")
            return 1

        print("\n" + "=" * 40)
        print("Connection validation completed successfully!")
        print("✓ Qdrant Cloud connection is working properly")
        return 0

    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("\nPlease ensure all required environment variables are set:")
        print("  - QDRANT_HOST")
        print("  - QDRANT_API_KEY")
        print("  - COLLECTION_NAME")
        print("  - COHERE_API_KEY")
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        logger.exception("Unexpected error during connection validation")
        return 1
    finally:
        # Ensure we disconnect from Qdrant
        try:
            if 'service' in locals():
                service.disconnect()
                print("✓ Disconnected from Qdrant Cloud")
        except:
            pass  # Ignore errors during disconnect

if __name__ == "__main__":
    sys.exit(main())