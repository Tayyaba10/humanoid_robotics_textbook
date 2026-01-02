"""
End-to-end integration tests for the RAG retrieval CLI tool.

These tests verify the complete workflow of the retrieve.py module.
"""
import unittest
import sys
import os
import argparse
from unittest.mock import patch, MagicMock

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.src.cli.retrieve import (
    setup_arg_parser,
    load_configuration,
    connect_to_qdrant,
    connect_to_cohere,
    generate_query_embeddings,
    perform_semantic_search,
    format_results,
    display_results,
    main,
    ConfigurationError,
    RAGRetrievalError
)


class TestEndToEndIntegration(unittest.TestCase):
    """Test cases for end-to-end integration."""

    @patch('backend.src.cli.retrieve.os.getenv')
    def test_setup_and_load_configuration(self, mock_getenv):
        """Test the configuration setup and loading process."""
        # Mock environment variables
        mock_getenv.side_effect = lambda x: {
            'QDRANT_HOST': 'https://test.qdrant.tech',
            'QDRANT_API_KEY': 'test-key',
            'COLLECTION_NAME': 'test-collection',
            'COHERE_API_KEY': 'test-cohere-key'
        }.get(x, None)

        config = load_configuration()

        self.assertEqual(config['qdrant_host'], 'https://test.qdrant.tech')
        self.assertEqual(config['qdrant_api_key'], 'test-key')
        self.assertEqual(config['collection_name'], 'test-collection')
        self.assertEqual(config['cohere_api_key'], 'test-cohere-key')

    def test_argument_parser(self):
        """Test the argument parser setup."""
        parser = setup_arg_parser()

        # Test with sample arguments
        args = parser.parse_args(['--query', 'test query', '--top_k', '5'])

        self.assertEqual(args.query, 'test query')
        self.assertEqual(args.top_k, 5)

    def test_argument_parser_defaults(self):
        """Test the argument parser with default values."""
        parser = setup_arg_parser()

        # Test with only required argument
        args = parser.parse_args(['--query', 'test query'])

        self.assertEqual(args.query, 'test query')
        self.assertEqual(args.top_k, 5)  # Default value

    @patch('cohere.Client')
    def test_generate_query_embeddings(self, mock_cohere_client):
        """Test the query embedding generation."""
        # Mock the Cohere client and response
        mock_client = MagicMock()
        mock_client.embed.return_value = MagicMock()
        mock_client.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]

        embeddings = generate_query_embeddings(mock_client, "test query")

        self.assertEqual(embeddings, [0.1, 0.2, 0.3])
        mock_client.embed.assert_called_once_with(texts=["test query"], model="embed-multilingual-v2.0")

    def test_format_results(self):
        """Test the result formatting."""
        # Mock search result object
        mock_result = MagicMock()
        mock_result.payload = {
            'content': 'Test content for the result',
            'source': 'test_source.txt',
            'chunk_index': 5
        }
        mock_result.score = 0.85

        formatted = format_results([mock_result])

        self.assertEqual(len(formatted), 1)
        self.assertEqual(formatted[0]['content_text'], 'Test content for the result')
        self.assertEqual(formatted[0]['source_document'], 'test_source.txt')
        self.assertEqual(formatted[0]['chunk_index'], 5)
        self.assertEqual(formatted[0]['similarity_score'], 0.85)

    @patch('sys.argv', ['retrieve.py', '--query', 'test query', '--top_k', '2'])
    @patch('os.getenv')
    @patch('backend.src.cli.retrieve.connect_to_qdrant')
    @patch('backend.src.cli.retrieve.connect_to_cohere')
    @patch('backend.src.cli.retrieve.generate_query_embeddings')
    @patch('backend.src.cli.retrieve.perform_semantic_search')
    @patch('backend.src.cli.retrieve.format_results')
    @patch('backend.src.cli.retrieve.display_results')
    def test_main_function_flow(self, mock_display, mock_format, mock_search,
                               mock_generate, mock_cohere, mock_qdrant, mock_getenv):
        """Test the main function flow with mocked dependencies."""
        # Mock environment variables
        mock_getenv.side_effect = lambda x: {
            'QDRANT_HOST': 'https://test.qdrant.tech',
            'QDRANT_API_KEY': 'test-key',
            'COLLECTION_NAME': 'test-collection',
            'COHERE_API_KEY': 'test-cohere-key'
        }.get(x, None)

        # Mock the various components
        mock_qdrant_client = MagicMock()
        mock_cohere_client = MagicMock()
        mock_qdrant.return_value = mock_qdrant_client
        mock_cohere.return_value = mock_cohere_client
        mock_generate.return_value = [0.1, 0.2, 0.3]
        mock_search.return_value = [MagicMock(), MagicMock()]
        mock_format.return_value = [
            {
                'content_text': 'Test content 1',
                'source_document': 'doc1.txt',
                'chunk_index': 1,
                'similarity_score': 0.9
            },
            {
                'content_text': 'Test content 2',
                'source_document': 'doc2.txt',
                'chunk_index': 2,
                'similarity_score': 0.8
            }
        ]

        # Call main function (we'll catch SystemExit if it occurs)
        try:
            main()
        except SystemExit:
            # Expected behavior when main completes normally
            pass

        # Verify all steps were called
        mock_qdrant.assert_called_once()
        mock_cohere.assert_called_once()
        mock_generate.assert_called_once()
        mock_search.assert_called_once()
        mock_format.assert_called_once()
        mock_display.assert_called_once()

    def test_display_results_output(self):
        """Test the display results function."""
        import io
        from contextlib import redirect_stdout

        formatted_results = [
            {
                'content_text': 'This is a test content that might be long',
                'source_document': 'test_source.txt',
                'chunk_index': 5,
                'similarity_score': 0.85
            }
        ]

        # Capture the output
        f = io.StringIO()
        with redirect_stdout(f):
            display_results(formatted_results)

        output = f.getvalue()

        # Check that the output contains expected elements
        self.assertIn("[1]", output)
        self.assertIn("Score: 0.85", output)
        self.assertIn("Source: test_source.txt", output)
        self.assertIn("Chunk: 5", output)
        self.assertIn("Text: This is a test content that might be", output)


if __name__ == '__main__':
    unittest.main()