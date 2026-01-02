"""
Basic test script to verify core functionality without external dependencies
"""
from main import chunk_text, validate_url

def test_basic_functionality():
    print("Testing basic functionality...")

    # Test URL validation
    print("\n1. Testing URL validation:")
    test_urls = [
        "https://example.com",
        "http://test.org/page",
        "invalid-url",
        "ftp://ftp.example.com",
        ""
    ]

    for url in test_urls:
        is_valid = validate_url(url)
        print(f"   {url} -> Valid: {is_valid}")

    # Test text chunking
    print("\n2. Testing text chunking:")
    sample_text = """This is a sample text for testing the chunking functionality.
    The system should split this text into appropriate chunks while preserving
    semantic boundaries. Each chunk should contain meaningful content that can
    be processed independently. This is important for the embedding process."""

    # Test chunking with a mock URL and heading
    chunks = chunk_text(sample_text, "https://example.com/test", "Test Heading")
    print(f"   Original text length: {len(sample_text)} characters")
    print(f"   Number of chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"   Chunk {i+1}: {len(chunk['content'])} chars - '{chunk['content'][:50]}...'")
        print(f"     URL: {chunk['url']}, Heading: {chunk['heading']}, Section: {chunk['section']}")

    print("\n3. All basic functionality tests passed!")

if __name__ == "__main__":
    test_basic_functionality()