import unittest
from unittest.mock import MagicMock, patch
import sys
from datetime import datetime

# Local mock of dependencies for importing the module under test
# This avoids global side effects if tests were run in a different environment
def setup_mocks():
    mock_modules = [
        "click", "mcp", "mcp.types", "mcp.server.lowlevel", "crawl4ai",
        "crawl4ai.content_scraping_strategy", "crawl4ai.deep_crawling",
        "starlette", "starlette.applications", "starlette.routing", "uvicorn",
        "mcp.server.sse", "mcp.server.stdio", "anyio"
    ]
    for module in mock_modules:
        if module not in sys.modules:
            sys.modules[module] = MagicMock()

setup_mocks()

# Ensure src is in path
if "src" not in sys.path:
    sys.path.insert(0, "src")

from crawl4ai_mcp import _format_markdown_page

class TestFormatMarkdownPage(unittest.TestCase):
    """
    Test suite for the _format_markdown_page function.
    Covers nominal cases, missing/partial metadata, and content sanitization.
    """
    def setUp(self):
        self.mock_result = MagicMock()
        self.mock_result.url = "https://example.com"
        self.mock_result.metadata = {
            "title": "Example Page",
            "depth": 2
        }
        self.text_content = "This is a [link](https://example.com) and some text."

    @patch("crawl4ai_mcp.datetime")
    def test_format_markdown_page_nominal(self, mock_datetime):
        """Test formatting with all required metadata present."""
        fixed_now = datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.now.return_value = fixed_now

        result_str = _format_markdown_page(self.mock_result, self.text_content)

        self.assertIn("# Example Page", result_str)
        self.assertIn("## URL\nhttps://example.com", result_str)
        self.assertIn("- Depth: 2", result_str)
        self.assertIn(f"- Timestamp: {fixed_now.isoformat()}", result_str)
        # Verify link removal
        self.assertIn("This is a link and some text.", result_str)
        self.assertNotIn("[link](https://example.com)", result_str)

    @patch("crawl4ai_mcp.datetime")
    def test_format_markdown_page_missing_metadata(self, mock_datetime):
        """Test fallback values when metadata attribute is missing."""
        del self.mock_result.metadata

        fixed_now = datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.now.return_value = fixed_now

        result_str = _format_markdown_page(self.mock_result, self.text_content)

        self.assertIn("# Untitled page", result_str)
        self.assertIn("- Depth: N/A", result_str)

    @patch("crawl4ai_mcp.datetime")
    def test_format_markdown_page_partial_metadata(self, mock_datetime):
        """Test fallback values when specific metadata keys are missing."""
        self.mock_result.metadata = {"title": "Partial Page"}

        fixed_now = datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.now.return_value = fixed_now

        result_str = _format_markdown_page(self.mock_result, self.text_content)

        self.assertIn("# Partial Page", result_str)
        self.assertIn("- Depth: N/A", result_str)

    @patch("crawl4ai_mcp.datetime")
    def test_format_markdown_page_with_images(self, mock_datetime):
        """Test that images are removed from the markdown content."""
        text_with_images = "Check this ![image](https://example.com/img.png) out."

        result_str = _format_markdown_page(self.mock_result, text_with_images)

        # Verify the original image markdown is gone
        self.assertNotIn("![image](https://example.com/img.png)", result_str)

if __name__ == "__main__":
    unittest.main()
