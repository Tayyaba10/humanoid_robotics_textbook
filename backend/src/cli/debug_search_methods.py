#!/usr/bin/env python3
"""
Debug script to identify available search methods in the qdrant-client version
"""
import os
import sys

def check_qdrant_client():
    try:
        from qdrant_client import QdrantClient
        print("✓ qdrant-client imported successfully")

        # Create a client instance (without connecting to check methods)
        # We'll use dummy values to create the client object
        client = QdrantClient(url="https://dummy.example.com", api_key="dummy")

        # Get all methods that contain 'search' or 'query'
        all_methods = [method for method in dir(client) if not method.startswith('_')]
        search_methods = [method for method in all_methods if 'search' in method.lower()]
        query_methods = [method for method in all_methods if 'query' in method.lower() and 'search' not in method.lower()]

        print(f"Found {len(search_methods)} search-related methods:")
        for method in search_methods:
            print(f"  - {method}")

        print(f"\nFound {len(query_methods)} query-related methods:")
        for method in query_methods:
            print(f"  - {method}")

        # Check for specific methods that are commonly used
        common_methods = ['search', 'search_points', 'points', 'search_batch', 'query']
        print(f"\nChecking for common methods:")
        for method in common_methods:
            exists = hasattr(client, method)
            print(f"  - {method}: {'✓' if exists else '✗'}")

        # If points exists, check its methods too
        if hasattr(client, 'points'):
            print(f"\nMethods in client.points:")
            points_methods = [method for method in dir(client.points) if 'search' in method.lower() or 'query' in method.lower()]
            for method in points_methods:
                print(f"  - points.{method}")

        return True
    except ImportError:
        print("✗ qdrant-client is not installed")
        return False
    except Exception as e:
        print(f"✗ Error checking qdrant-client: {e}")
        return False

if __name__ == "__main__":
    print("Checking qdrant-client installation and available methods...")
    success = check_qdrant_client()
    if success:
        print("\n✓ qdrant-client check completed")
    else:
        print("\n✗ qdrant-client check failed")