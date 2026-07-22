import os
import sys
import unittest
from unittest.mock import patch

# Mock out heavy dependencies that might not be available or fail to load


# Now we can import from our module safely
sys.path.append(os.path.join(os.getcwd(), "src"))
from crawl4ai_mcp_llm.crawler import crawl_and_output_to_markdown

class TestSecurityJS(unittest.IsolatedAsyncioTestCase):
    async def test_js_code_blocked_by_default(self):
        # Ensure environment variable is not set
        if "CRAWL4AI_MCP_ALLOW_JS" in os.environ:
            del os.environ["CRAWL4AI_MCP_ALLOW_JS"]

        result = await crawl_and_output_to_markdown(
            "https://example.com",
            js_code="console.log('malicious code')"
        )

        self.assertIn("error", result)
        self.assertIn("Custom JavaScript execution is disabled", result["error"])
        self.assertIsNone(result["file_path"])
        self.assertEqual(result["stats"]["successful_pages"], 0)

    async def test_js_code_blocked_when_explicitly_false(self):
        with patch.dict(os.environ, {"CRAWL4AI_MCP_ALLOW_JS": "false"}):
            result = await crawl_and_output_to_markdown(
                "https://example.com",
                js_code="console.log('malicious code')"
            )

            self.assertIn("error", result)
            self.assertIn("Custom JavaScript execution is disabled", result["error"])

    @patch("crawl4ai_mcp_llm.crawler.AsyncWebCrawler")
    @patch("crawl4ai_mcp_llm.crawler.results_to_markdown")
    async def test_js_code_allowed_when_env_set_to_true(self, mock_results_to_markdown, mock_crawler_class):
        with patch.dict(os.environ, {"CRAWL4AI_MCP_ALLOW_JS": "true"}):
            # Setup mocks for successful crawl
            mock_crawler = mock_crawler_class.return_value.__aenter__.return_value
            mock_crawler.arun.return_value = []
            mock_results_to_markdown.return_value = {"error": None, "file_path": "test.md", "stats": {"successful_pages": 1}}

            result = await crawl_and_output_to_markdown(
                "https://example.com",
                js_code="console.log('legit code')"
            )

            # Should not return the security error
            if result.get("error"):
                self.assertNotIn("Custom JavaScript execution is disabled", result["error"])

            # Verify that js_code was passed to CrawlerRunConfig (implicitly via arun call)
            args, kwargs = mock_crawler.arun.call_args
            config = kwargs.get("config")
            self.assertEqual(config.js_code, "console.log('legit code')")

if __name__ == "__main__":
    unittest.main()
