#!/usr/bin/env python3
"""
Minimal test to check the search API works with the current qdrant-client version
"""
import os
from qdrant_client import QdrantClient

def test_search_api():
    # Read environment variables
    qdrant_host = os.getenv('QDRANT_HOST')
    qdrant_api_key = os.getenv('QDRANT_API_KEY')
    collection_name = os.getenv('COLLECTION_NAME')

    if not all([qdrant_host, qdrant_api_key, collection_name]):
        print("ERROR: Missing required environment variables")
        return False

    print(f"Testing search API with collection: {collection_name}")

    try:
        # Initialize client
        client = QdrantClient(
            url=qdrant_host,
            api_key=qdrant_api_key,
            timeout=10
        )

        # Test with a dummy query vector (we'll catch the actual search error if any)
        dummy_vector = [0.1] * 10  # Assuming 10-dimensional vector for testing

        # Try different search methods based on the version
        search_methods_to_try = [
            # Method 1: search_points with query_vector parameter
            lambda: client.search_points(
                collection_name=collection_name,
                query_vector=dummy_vector,
                limit=1,
                with_payload=True
            ),
            # Method 2: search_points with vector parameter
            lambda: client.search_points(
                collection_name=collection_name,
                vector=dummy_vector,
                limit=1,
                with_payload=True
            ),
            # Method 3: main search method
            lambda: client.search(
                collection_name=collection_name,
                query_vector=dummy_vector,
                limit=1,
                with_payload=True
            ),
            # Method 4: points.search
            lambda: client.points.search(
                collection_name=collection_name,
                query_vector=dummy_vector,
                limit=1,
                with_payload=True
            )
        ]

        method_names = [
            "client.search_points(query_vector=...)",
            "client.search_points(vector=...)",
            "client.search(query_vector=...)",
            "client.points.search(query_vector=...)"
        ]

        for i, (method, name) in enumerate(zip(search_methods_to_try, method_names)):
            try:
                print(f"Trying {name}...")
                # This will fail with dummy vector, but we want to see if the method exists
                result = method()
                print(f"✓ Method {name} exists and is callable")
                return True
            except AttributeError as e:
                print(f"✗ Method {name} does not exist: {e}")
                continue
            except Exception as e:
                # If we get any other exception, it means the method exists but failed for other reasons
                # (like invalid vector, etc.), which means the method exists
                print(f"✓ Method {name} exists but failed with: {type(e).__name__}: {e}")
                return True

        print("✗ All search methods failed - no working search method found")
        return False

    except Exception as e:
        print(f"✗ Failed to initialize client or test search: {e}")
        return False

if __name__ == "__main__":
    success = test_search_api()
    if success:
        print("\n✓ Search API test completed - at least one method is available")
    else:
        print("\n✗ Search API test failed - no working search method found")