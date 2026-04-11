import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Mocking all external dependencies to avoid ModuleNotFoundError
mock_mcp = MagicMock()
mock_crawl4ai = MagicMock()
mock_starlette = MagicMock()
mock_uvicorn = MagicMock()
mock_anyio = MagicMock()
mock_click = MagicMock()

sys.modules["anyio"] = mock_anyio
sys.modules["click"] = mock_click
sys.modules["mcp"] = mock_mcp
sys.modules["mcp.types"] = mock_mcp.types
sys.modules["mcp.server"] = mock_mcp.server
sys.modules["mcp.server.lowlevel"] = mock_mcp.server.lowlevel
sys.modules["mcp.server.sse"] = mock_mcp.server.sse
sys.modules["mcp.server.stdio"] = mock_mcp.server.stdio
sys.modules["crawl4ai"] = mock_crawl4ai
sys.modules["crawl4ai.content_scraping_strategy"] = mock_crawl4ai.content_scraping_strategy
sys.modules["crawl4ai.deep_crawling"] = mock_crawl4ai.deep_crawling
sys.modules["starlette"] = mock_starlette
sys.modules["starlette.applications"] = mock_starlette.applications
sys.modules["starlette.routing"] = mock_starlette.routing
sys.modules["uvicorn"] = mock_uvicorn

# Now import the function to test
from crawl4ai_mcp import run_sse_server

class TestSecurityDebug(unittest.TestCase):
    @patch("crawl4ai_mcp.Starlette")
    @patch("crawl4ai_mcp.uvicorn")
    @patch("crawl4ai_mcp.SseServerTransport")
    def test_run_sse_server_debug_false_by_default(self, mock_sse_transport, mock_uvicorn, mock_starlette_class):
        # Ensure environment variable is not set
        if "CRAWL4AI_MCP_DEBUG" in os.environ:
            del os.environ["CRAWL4AI_MCP_DEBUG"]

        mock_app = MagicMock()
        run_sse_server(mock_app, 8000)

        # Check that Starlette was initialized with debug=False
        args, kwargs = mock_starlette_class.call_args
        self.assertFalse(kwargs.get("debug"))

    @patch("crawl4ai_mcp.Starlette")
    @patch("crawl4ai_mcp.uvicorn")
    @patch("crawl4ai_mcp.SseServerTransport")
    def test_run_sse_server_debug_true_when_env_set(self, mock_sse_transport, mock_uvicorn, mock_starlette_class):
        with patch.dict(os.environ, {"CRAWL4AI_MCP_DEBUG": "true"}):
            mock_app = MagicMock()
            run_sse_server(mock_app, 8000)

            # Check that Starlette was initialized with debug=True
            args, kwargs = mock_starlette_class.call_args
            self.assertTrue(kwargs.get("debug"))

    @patch("crawl4ai_mcp.Starlette")
    @patch("crawl4ai_mcp.uvicorn")
    @patch("crawl4ai_mcp.SseServerTransport")
    def test_run_sse_server_debug_false_when_env_set_to_false(self, mock_sse_transport, mock_uvicorn, mock_starlette_class):
        with patch.dict(os.environ, {"CRAWL4AI_MCP_DEBUG": "false"}):
            mock_app = MagicMock()
            run_sse_server(mock_app, 8000)

            # Check that Starlette was initialized with debug=False
            args, kwargs = mock_starlette_class.call_args
            self.assertFalse(kwargs.get("debug"))

if __name__ == "__main__":
    unittest.main()
