import unittest
import re
from unittest.mock import MagicMock
import sys
import os

# Add src to sys.path
sys.path.append(os.path.abspath("src"))

# Mocking modules that might fail to import
mock_modules = ["anyio", "click", "uvicorn", "mcp", "mcp.types", "mcp.server", "mcp.server.lowlevel", "mcp.server.sse", "mcp.server.stdio", "crawl4ai", "crawl4ai.content_scraping_strategy", "crawl4ai.deep_crawling", "starlette", "starlette.applications", "starlette.routing"]
for mod in mock_modules:
    sys.modules[mod] = MagicMock()

import crawl4ai_mcp

class TestErrorDetection(unittest.TestCase):
    def test_extract_page_content_and_errors_regex(self):
        # Case: 404 in title
        mock_result = MagicMock()
        mock_result.markdown = "Some content"
        mock_result.metadata = {"title": "404 Not Found"}

        content, error_type = crawl4ai_mcp._extract_page_content_and_errors(mock_result)
        self.assertEqual(error_type, "404")
        self.assertEqual(content, "Some content")

        # Case: Forbidden in title
        mock_result.metadata = {"title": "Forbidden Access"}
        content, error_type = crawl4ai_mcp._extract_page_content_and_errors(mock_result)
        self.assertEqual(error_type, "403")

        # Case: Normal title
        mock_result.metadata = {"title": "Welcome to my page"}
        content, error_type = crawl4ai_mcp._extract_page_content_and_errors(mock_result)
        self.assertIsNone(error_type)

    def test_extract_page_content_and_errors_nginx(self):
        # Case: nginx error page
        mock_result = MagicMock()
        mock_result.markdown = "404 Not Found nginx"
        mock_result.metadata = {"title": "Home"}

        content, error_type = crawl4ai_mcp._extract_page_content_and_errors(mock_result)
        self.assertEqual(error_type, "404")

if __name__ == "__main__":
    unittest.main()
