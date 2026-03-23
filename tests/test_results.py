from unittest.mock import patch
import pytest
import anyio
import os
from crawl4ai_mcp import results_to_markdown, _extract_page_content_and_errors, crawl_and_output_to_markdown

class MockResult:
    def __init__(self, i, error_type=None):
        self.url = f"https://example.com/page{i}"

        if error_type == "missing":
            self.markdown = None
            self.metadata = {"title": "No content", "depth": 1}
        elif error_type == "404":
            self.markdown = "404 Not Found nginx"
            self.metadata = {"title": "404 Not Found", "depth": 1}
        elif error_type == "403":
            self.markdown = "403 Forbidden nginx"
            self.metadata = {"title": "403 Forbidden", "depth": 1}
        else:
            self.markdown = f"# Page {i}\nTest content."
            self.metadata = {"title": f"Test Page {i}", "depth": 1}

        self.links = {
            "internal": [{"href": f"https://example.com/page{i}/subpage"}],
            "external": [{"href": "https://external.com"}]
        }

@pytest.mark.anyio
async def test_results_to_markdown_success():
    results = [MockResult(1), MockResult(2)]
    output_path = "test_output.md"

    try:
        res = await results_to_markdown(results, output_path)

        assert res["error"] is None
        assert res["file_path"] == output_path
        assert res["stats"]["successful_pages"] == 2
        assert res["stats"]["failed_pages"] == 0
        assert res["stats"]["not_found_pages"] == 0

        # Verify file contents
        assert os.path.exists(output_path)
        async with await anyio.Path(output_path).open("r") as f:
            content = await f.read()
            assert "# Test Page 1" in content
            assert "# Test Page 2" in content

    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

@pytest.mark.anyio
async def test_results_to_markdown_with_errors():
    results = [
        MockResult(1),
        MockResult(2, error_type="missing"),
        MockResult(3, error_type="404"),
        MockResult(4, error_type="403")
    ]
    output_path = "test_output_errors.md"

    try:
        res = await results_to_markdown(results, output_path)

        assert res["error"] is None
        assert res["stats"]["successful_pages"] == 1
        assert res["stats"]["failed_pages"] == 1
        assert res["stats"]["not_found_pages"] == 1
        assert res["stats"]["forbidden_pages"] == 1

    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

@pytest.mark.anyio
async def test_results_to_markdown_exception():
    results = [MockResult(1)]
    output_path = "test_output_exception.md"

    # Mock anyio.Path.open to raise an exception
    with patch("anyio.Path.open", side_effect=PermissionError("Permission denied")):
        res = await results_to_markdown(results, output_path)

        assert "error" in res
        assert res["error"] == "Writing error: Permission denied"


def test_extract_page_content_and_errors_404_text_with_nginx():
    class MockResultTextError:
        markdown = "An error occurred: 404 Not Found nginx"
        metadata = {"title": "Normal Title", "depth": 1}

    result = MockResultTextError()
    content, error_type = _extract_page_content_and_errors(result)
    assert content == "An error occurred: 404 Not Found nginx"
    assert error_type == "404"

def test_extract_page_content_and_errors_403_text_with_nginx():
    class MockResultTextError:
        markdown = "An error occurred: 403 Forbidden nginx"
        metadata = {"title": "Normal Title", "depth": 1}

    result = MockResultTextError()
    content, error_type = _extract_page_content_and_errors(result)
    assert content == "An error occurred: 403 Forbidden nginx"
    assert error_type == "403"

def test_extract_page_content_and_errors_404_title():
    class MockResultTitleError:
        markdown = "Some normal looking content without the n word"
        metadata = {"title": "Page 404 Not Found", "depth": 1}

    result = MockResultTitleError()
    content, error_type = _extract_page_content_and_errors(result)
    assert content == "Some normal looking content without the n word"
    assert error_type == "404"

def test_extract_page_content_and_errors_403_title():
    class MockResultTitleError:
        markdown = "Some normal looking content"
        metadata = {"title": "Access Forbidden Error", "depth": 1}

    result = MockResultTitleError()
    content, error_type = _extract_page_content_and_errors(result)
    assert content == "Some normal looking content"
    assert error_type == "403"

def test_extract_page_content_and_errors_missing():
    class MockResultMissing:
        markdown = None
        text = None
        metadata = {"title": "Normal Title", "depth": 1}

    result = MockResultMissing()
    content, error_type = _extract_page_content_and_errors(result)
    assert content is None
    assert error_type == "missing"

def test_extract_page_content_and_errors_normal():
    class MockResultNormal:
        markdown = "This is a great page"
        metadata = {"title": "Great Page", "depth": 1}

    result = MockResultNormal()
    content, error_type = _extract_page_content_and_errors(result)
    assert content == "This is a great page"
    assert error_type is None


@pytest.mark.anyio
async def test_crawl_and_output_to_markdown_exception():
    class MockCrawlerContext:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def arun(self, url, **kwargs):
            raise Exception("Simulated crawl error")

    with patch("crawl4ai_mcp.AsyncWebCrawler", return_value=MockCrawlerContext()):
        result = await crawl_and_output_to_markdown("https://example.com")

        assert "error" in result
        assert result["error"] == "Crawling error: Simulated crawl error"
        assert result["file_path"] is None
        assert "stats" in result
        assert result["stats"]["successful_pages"] == 0
        assert result["stats"]["failed_pages"] == 0
        assert result["stats"]["not_found_pages"] == 0
        assert result["stats"]["forbidden_pages"] == 0
        assert result["stats"]["duration_seconds"] == 0
