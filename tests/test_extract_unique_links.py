import sys
from unittest.mock import MagicMock

# Mock dependencies
sys.modules["anyio"] = MagicMock()
sys.modules["click"] = MagicMock()
sys.modules["uvicorn"] = MagicMock()
sys.modules["mcp"] = MagicMock()
sys.modules["mcp.types"] = MagicMock()
sys.modules["mcp.server"] = MagicMock()
sys.modules["mcp.server.lowlevel"] = MagicMock()
sys.modules["mcp.server.sse"] = MagicMock()
sys.modules["mcp.server.stdio"] = MagicMock()
sys.modules["crawl4ai"] = MagicMock()
sys.modules["crawl4ai.content_scraping_strategy"] = MagicMock()
sys.modules["crawl4ai.deep_crawling"] = MagicMock()
sys.modules["starlette"] = MagicMock()
sys.modules["starlette.applications"] = MagicMock()
sys.modules["starlette.routing"] = MagicMock()

import pytest
from crawl4ai_mcp import _extract_unique_links

class MockCrawlResult:
    def __init__(self, links=None, has_links_attr=True):
        if has_links_attr:
            self.links = links

def test_extract_unique_links_basic():
    results = [
        MockCrawlResult(links={
            "internal": [{"href": "https://example.com/a", "text": "A"}],
            "external": [{"href": "https://google.com", "text": "Google"}]
        }),
        MockCrawlResult(links={
            "internal": [{"href": "https://example.com/b", "text": "B"}],
            "external": [{"href": "https://github.com", "text": "GitHub"}]
        })
    ]

    extracted = _extract_unique_links(results)

    assert len(extracted["internal"]) == 2
    assert len(extracted["external"]) == 2
    assert extracted["internal"][0]["href"] == "https://example.com/a"
    assert extracted["internal"][1]["href"] == "https://example.com/b"
    assert extracted["external"][0]["href"] == "https://google.com"
    assert extracted["external"][1]["href"] == "https://github.com"

def test_extract_unique_links_deduplication():
    results = [
        MockCrawlResult(links={
            "internal": [{"href": "https://example.com/a", "text": "A1"}],
            "external": [{"href": "https://google.com", "text": "Google1"}]
        }),
        MockCrawlResult(links={
            "internal": [{"href": "https://example.com/a", "text": "A2"}],
            "external": [{"href": "https://google.com", "text": "Google2"}]
        })
    ]

    extracted = _extract_unique_links(results)

    # Should only have 1 of each because href is the same
    assert len(extracted["internal"]) == 1
    assert len(extracted["external"]) == 1
    assert extracted["internal"][0]["text"] == "A1"
    assert extracted["external"][0]["text"] == "Google1"

def test_extract_unique_links_missing_attr():
    results = [
        MockCrawlResult(has_links_attr=False),
        MockCrawlResult(links={
            "internal": [{"href": "https://example.com/a"}]
        })
    ]

    extracted = _extract_unique_links(results)
    assert len(extracted["internal"]) == 1
    assert extracted["internal"][0]["href"] == "https://example.com/a"

def test_extract_unique_links_not_dict():
    results = [
        MockCrawlResult(links=["not", "a", "dict"]),
        MockCrawlResult(links={
            "internal": [{"href": "https://example.com/a"}]
        })
    ]

    extracted = _extract_unique_links(results)
    assert len(extracted["internal"]) == 1
    assert extracted["internal"][0]["href"] == "https://example.com/a"

def test_extract_unique_links_empty_input():
    extracted = _extract_unique_links([])
    assert extracted == {"internal": [], "external": []}

def test_extract_unique_links_missing_keys():
    results = [
        MockCrawlResult(links={
            "internal": [{"href": "https://example.com/a"}]
            # external missing
        }),
        MockCrawlResult(links={
            "external": [{"href": "https://google.com"}]
            # internal missing
        })
    ]

    extracted = _extract_unique_links(results)
    assert len(extracted["internal"]) == 1
    assert len(extracted["external"]) == 1
    assert extracted["internal"][0]["href"] == "https://example.com/a"
    assert extracted["external"][0]["href"] == "https://google.com"

def test_extract_unique_links_no_href():
    results = [
        MockCrawlResult(links={
            "internal": [{"text": "No href"}]
        })
    ]

    extracted = _extract_unique_links(results)
    assert len(extracted["internal"]) == 0

def test_extract_unique_links_not_a_list():
    results = [
        MockCrawlResult(links={
            "internal": "not a list",
            "external": [{"href": "https://google.com"}]
        })
    ]

    # The current implementation of _extract_unique_links:
    # for link in result.links[k]:
    # will raise TypeError if result.links[k] is not iterable (like a string, though a string IS iterable)
    # but it will crash if it is e.g. an integer.
    # Actually, if it's a string "not a list", it will iterate over characters and link.get('href') will fail.

    with pytest.raises(Exception): # Exact exception depends on the type
        _extract_unique_links(results)
