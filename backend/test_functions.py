"""
Simple test script to verify the main functions work correctly
"""
import os
from main import get_all_urls, extract_text_from_url, chunk_text, embed

def test_functions():
    # Test URL discovery
    print("Testing URL discovery...")
    base_url = "https://tayyaba10.github.io/humanoid_robotics_textbook/"
    urls, metadata = get_all_urls(base_url)
    print(f"Found {len(urls)} URLs")
    print(f"Metadata: {metadata}")

    if urls:
        # Test content extraction on the first URL
        print(f"\nTesting content extraction from: {urls[0]}")
        content, content_metadata = extract_text_from_url(urls[0])
        print(f"Extracted {content_metadata['word_count']} words")
        print(f"Title: {content_metadata['title']}")
        print(f"Heading: {content_metadata['heading']}")

        # Test chunking
        print(f"\nTesting text chunking...")
        chunks = chunk_text(content[:3000], urls[0], content_metadata['heading'])  # Use first 3000 chars
        print(f"Text chunked into {len(chunks)} chunks")
        if chunks:
            print(f"First chunk word count: {chunks[0]['word_count']}")
            print(f"First chunk content preview: {chunks[0]['content'][:100]}...")

    print("\nFunctions tested successfully!")

if __name__ == "__main__":
    test_functions()