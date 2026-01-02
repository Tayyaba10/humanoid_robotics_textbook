"""
Unit tests for the RAG retrieval CLI tool.

These tests verify the functionality of individual components in the retrieve.py module.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.src.cli.retrieve import (
    validate_host_format,
    load_configuration,
    format_results,
    display_results,
    generate_query_embeddings,
    perform_semantic_search,
    verify_collection_exists,
    connect_to_qdrant,
    connect_to_cohere,
    retry_with_backoff,
    ConfigurationError,
    RAGRetrievalError
)


class TestHostValidation(unittest.TestCase):
    """Test cases for host format validation."""

    def test_valid_http_url(self):
        """Test that valid HTTP URLs are accepted."""
        self.assertTrue(validate_host_format("http://localhost:6333"))
        self.assertTrue(validate_host_format("http://example.com:6333"))
        self.assertTrue(validate_host_format("http://192.168.1.1:6333"))

    def test_valid_https_url(self):
        """Test that valid HTTPS URLs are accepted."""
        self.assertTrue(validate_host_format("https://example.com:6333"))
        self.assertTrue(validate_host_format("https://qdrant.example.com"))

    def test_valid_host_port(self):
        """Test that valid host:port formats are accepted."""
        self.assertTrue(validate_host_format("localhost:6333"))
        self.assertTrue(validate_host_format("example.com:6333"))
        self.assertTrue(validate_host_format("192.168.1.1:6333"))

    def test_invalid_formats(self):
        """Test that invalid formats are rejected."""
        self.assertFalse(validate_host_format(""))
        self.assertFalse(validate_host_format("not-a-url"))
        self.assertFalse(validate_host_format("ftp://example.com"))


class TestConfigurationLoading(unittest.TestCase):
    """Test cases for configuration loading."""

    @patch.dict(os.environ, {
        'QDRANT_HOST': 'https://example.com',
        'QDRANT_API_KEY': 'test-key',
        'COLLECTION_NAME': 'test-collection',
        'COHERE_API_KEY': 'cohere-key'
    })
    def test_load_configuration_success(self):
        """Test successful configuration loading."""
        config = load_configuration()
        self.assertEqual(config['qdrant_host'], 'https://example.com')
        self.assertEqual(config['qdrant_api_key'], 'test-key')
        self.assertEqual(config['collection_name'], 'test-collection')
        self.assertEqual(config['cohere_api_key'], 'cohere-key')

    def test_load_configuration_missing_vars(self):
        """Test configuration loading with missing environment variables."""
        # Clear all relevant environment variables
        for var in ['QDRANT_HOST', 'QDRANT_API_KEY', 'COLLECTION_NAME', 'COHERE_API_KEY']:
            if var in os.environ:
                del os.environ[var]

        with self.assertRaises(ConfigurationError):
            load_configuration()


class TestResultFormatting(unittest.TestCase):
    """Test cases for result formatting."""

    def test_format_results_empty(self):
        """Test formatting of empty results."""
        formatted = format_results([])
        self.assertEqual(len(formatted), 0)

    def test_format_results_with_data(self):
        """Test formatting of results with data."""
        # Mock search result object
        mock_result = Mock()
        mock_result.payload = {
            'content': 'Test content',
            'source': 'test_source.txt',
            'chunk_index': 5
        }
        mock_result.score = 0.85

        formatted = format_results([mock_result])
        self.assertEqual(len(formatted), 1)
        self.assertEqual(formatted[0]['content_text'], 'Test content')
        self.assertEqual(formatted[0]['source_document'], 'test_source.txt')
        self.assertEqual(formatted[0]['chunk_index'], 5)
        self.assertEqual(formatted[0]['similarity_score'], 0.85)


class TestRetryLogic(unittest.TestCase):
    """Test cases for retry logic."""

    def test_retry_success_on_first_attempt(self):
        """Test that function succeeds on first attempt."""
        def success_func():
            return "success"

        result = retry_with_backoff(success_func, max_retries=2)
        self.assertEqual(result, "success")

    def test_retry_eventually_succeeds(self):
        """Test that function succeeds after a few failures."""
        attempts = 0
        def sometimes_fails():
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise Exception("Temporary failure")
            return "eventually successful"

        result = retry_with_backoff(sometimes_fails, max_retries=5)
        self.assertEqual(result, "eventually successful")
        self.assertEqual(attempts, 3)

    def test_retry_eventually_fails(self):
        """Test that function fails after all retries."""
        def always_fails():
            raise Exception("Permanent failure")

        with self.assertRaises(Exception) as context:
            retry_with_backoff(always_fails, max_retries=2)

        self.assertIn("Permanent failure", str(context.exception))


if __name__ == '__main__':
    unittest.main()