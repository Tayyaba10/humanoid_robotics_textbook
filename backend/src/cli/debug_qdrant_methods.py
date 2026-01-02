#!/usr/bin/env python3
"""Test script to identify available methods in QdrantClient"""
import os
from qdrant_client import QdrantClient

# Initialize client (without actually connecting)
host = os.getenv('QDRANT_HOST', 'https://test.qdrant.example.com')
api_key = os.getenv('QDRANT_API_KEY', 'test_api_key')

client = QdrantClient(
    url=host,
    api_key=api_key,
    timeout=10
)

# Print all available methods in the client
methods = [method for method in dir(client) if not method.startswith('_') and callable(getattr(client, method))]
print("Available methods in QdrantClient:")
for method in sorted(methods):
    print(f"  - {method}")

# Check for search-related methods specifically
search_methods = [method for method in methods if 'search' in method.lower()]
print(f"\nSearch-related methods: {search_methods}")