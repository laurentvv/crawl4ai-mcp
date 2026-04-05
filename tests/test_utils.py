import pytest
from crawl4ai_mcp import remove_links_from_markdown

def test_remove_links_basic():
    """Test that basic markdown links are replaced with their text."""
    text = "Check this [link](https://example.com) out."
    expected = "Check this link out."
    assert remove_links_from_markdown(text) == expected

def test_remove_images_basic():
    """Test that markdown images are completely removed."""
    text = "Here is an image: ![alt text](https://example.com/image.png)"
    expected = "Here is an image: "
    assert remove_links_from_markdown(text) == expected

def test_mixed_links_and_images():
    """Test handling of mixed links and images in the same text."""
    text = "A [link](url) and an ![image](img_url)."
    expected = "A link and an ."
    assert remove_links_from_markdown(text) == expected

def test_code_block_protection():
    """Test that links and images inside code blocks are preserved."""
    text = """
Here is some code:
```python
[this](is-not-a-link)
![and-this](is-not-an-image)
```
Outside the code: [link](url)
"""
    result = remove_links_from_markdown(text)
    assert "```python\n[this](is-not-a-link)\n![and-this](is-not-an-image)\n```" in result
    assert "Outside the code: link" in result

def test_whitespace_handling():
    """Test that extra spaces and empty lines are correctly handled."""
    text = "Too many    spaces and\n\n\nempty lines."
    result = remove_links_from_markdown(text)
    assert "Too many spaces" in result
    assert "\n\n" in result
