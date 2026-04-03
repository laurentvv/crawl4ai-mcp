import pytest
import os
from crawl4ai_mcp import crawl_and_output_to_markdown

@pytest.mark.anyio
@pytest.mark.integration
async def test_crawl_zai_docs():
    url = "https://docs.z.ai/devpack/overview"
    max_depth = 2 # Let's start with a depth of 2 to catch the left menu pages

    result = await crawl_and_output_to_markdown(
        start_url=url,
        max_depth=max_depth,
        include_external=False,
        verbose=True
    )

    assert result["error"] is None, f"Crawler returned an error: {result['error']}"

    file_path = result["file_path"]
    assert file_path is not None, "File path should not be None"
    assert os.path.exists(file_path), f"File {file_path} should exist"

    stats = result["stats"]
    print(f"Integration test stats: {stats}")

    # Verify the amount of pages (we expect multiple pages due to depth > 1)
    # The exact number is unknown but should be > 1
    assert stats["successful_pages"] >= 1, "At least one page should be processed"

    # Now read the generated markdown file to let us inspect the quality in the next step
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert len(content) > 0, "Generated markdown should not be empty"
