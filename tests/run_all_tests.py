import unittest
import sys
import os
from unittest.mock import MagicMock

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

if __name__ == "__main__":
    setup_mocks()

    # Ensure src is in path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    sys.exit(0 if result.wasSuccessful() else 1)
