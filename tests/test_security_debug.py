import unittest
from unittest.mock import MagicMock, patch
import os

# Mocking all external dependencies to avoid ModuleNotFoundError
mock_mcp = MagicMock()
mock_crawl4ai = MagicMock()
mock_starlette = MagicMock()
mock_uvicorn = MagicMock()
mock_anyio = MagicMock()
mock_click = MagicMock()


# Now import the function to test
from crawl4ai_mcp.cli import run_sse_server

class TestSecurityDebug(unittest.TestCase):
    @patch("crawl4ai_mcp.cli.Starlette")
    @patch("crawl4ai_mcp.cli.uvicorn")
    @patch("crawl4ai_mcp.cli.SseServerTransport")
    def test_run_sse_server_debug_false_by_default(self, mock_sse_transport, mock_uvicorn, mock_starlette_class):
        # Ensure environment variable is not set
        if "CRAWL4AI_MCP_DEBUG" in os.environ:
            del os.environ["CRAWL4AI_MCP_DEBUG"]

        mock_app = MagicMock()
        run_sse_server(mock_app, 8000)

        # Check that Starlette was initialized with debug=False
        args, kwargs = mock_starlette_class.call_args
        self.assertFalse(kwargs.get("debug"))

    @patch("crawl4ai_mcp.cli.Starlette")
    @patch("crawl4ai_mcp.cli.uvicorn")
    @patch("crawl4ai_mcp.cli.SseServerTransport")
    def test_run_sse_server_debug_true_when_env_set(self, mock_sse_transport, mock_uvicorn, mock_starlette_class):
        with patch.dict(os.environ, {"CRAWL4AI_MCP_DEBUG": "true"}):
            mock_app = MagicMock()
            run_sse_server(mock_app, 8000)

            # Check that Starlette was initialized with debug=True
            args, kwargs = mock_starlette_class.call_args
            self.assertTrue(kwargs.get("debug"))

    @patch("crawl4ai_mcp.cli.Starlette")
    @patch("crawl4ai_mcp.cli.uvicorn")
    @patch("crawl4ai_mcp.cli.SseServerTransport")
    def test_run_sse_server_debug_false_when_env_set_to_false(self, mock_sse_transport, mock_uvicorn, mock_starlette_class):
        with patch.dict(os.environ, {"CRAWL4AI_MCP_DEBUG": "false"}):
            mock_app = MagicMock()
            run_sse_server(mock_app, 8000)

            # Check that Starlette was initialized with debug=False
            args, kwargs = mock_starlette_class.call_args
            self.assertFalse(kwargs.get("debug"))

if __name__ == "__main__":
    unittest.main()
