#!/usr/bin/env python3
"""Test script to check the correct Qdrant search API"""
import os
from qdrant_client import QdrantClient

# Read environment variables
qdrant_host = os.getenv('QDRANT_HOST')
qdrant_api_key = os.getenv('QDRANT_API_KEY')
collection_name = os.getenv('COLLECTION_NAME')

if not all([qdrant_host, qdrant_api_key, collection_name]):
    print("Environment variables not set, using dummy values for testing API structure")
    qdrant_host = "https://test.qdrant.example.com"
    qdrant_api_key = "dummy_key"
    collection_name = "test_collection"

# Initialize client
client = QdrantClient(
    url=qdrant_host,
    api_key=qdrant_api_key,
    timeout=10
)

print("Available methods containing 'search':")
search_methods = [method for method in dir(client) if 'search' in method.lower() and not method.startswith('_')]
for method in search_methods:
    print(f"  - {method}")

print("\nTrying different search API approaches...")

# Test 1: Try the main search method
try:
    print("\n1. Testing client.search()...")
    # This will fail with dummy values, but we want to see if the method exists
    # We'll catch the AttributeError specifically
    import inspect
    sig = inspect.signature(client.search)
    print(f"   client.search signature: {sig}")
    print("   ✓ client.search method exists")
except AttributeError:
    print("   ✗ client.search method does NOT exist")
except Exception as e:
    print(f"   ? client.search method exists but call failed: {e}")

# Test 2: Try points.search
try:
    print("\n2. Testing client.points.search...")
    if hasattr(client, 'points') and hasattr(client.points, 'search'):
        import inspect
        sig = inspect.signature(client.points.search)
        print(f"   client.points.search signature: {sig}")
        print("   ✓ client.points.search method exists")
    else:
        print("   ✗ client.points.search method does NOT exist")
except Exception as e:
    print(f"   ? client.points.search exists but call failed: {e}")

# Test 3: Try search_points
try:
    print("\n3. Testing client.search_points...")
    import inspect
    sig = inspect.signature(client.search_points)
    print(f"   client.search_points signature: {sig}")
    print("   ✓ client.search_points method exists")
except AttributeError:
    print("   ✗ client.search_points method does NOT exist")
except Exception as e:
    print(f"   ? client.search_points exists but call failed: {e}")

# Test 4: Check what methods are available on the client object
print(f"\n4. All public methods in client object:")
public_methods = [method for method in dir(client) if not method.startswith('_')]
search_related = [method for method in public_methods if 'search' in method.lower()]
print(f"   Search-related: {search_related}")
print(f"   Total public methods: {len(public_methods)}")