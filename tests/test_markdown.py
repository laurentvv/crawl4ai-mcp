import pytest
from crawl4ai_mcp import remove_links_from_markdown

def test_remove_links():
    markdown = "Check this [link](http://example.com) and this [other link](https://test.org)."
    expected = "Check this link and this other link."
    assert remove_links_from_markdown(markdown) == expected

def test_remove_images():
    markdown = "Check this image: ![Alt text](http://example.com/image.png)"
    expected = "Check this image: "
    assert remove_links_from_markdown(markdown) == expected

def test_mixed_links_and_images():
    markdown = "Check this image: ![Alt text](http://example.com/image.png) and this link: [Example](http://example.com)"
    # With the fix, the image is removed entirely, and the link is converted to text
    expected = "Check this image: and this link: Example"
    assert remove_links_from_markdown(markdown) == expected

def test_preserve_code_blocks():
    markdown = """
Here is some code:
```python
def hello():
    print("[Link in code](http://example.com)")
```
And a link outside: [External](http://external.com)
"""
    expected = """
Here is some code:
```python
def hello():
    print("[Link in code](http://example.com)")
```
And a link outside: External
"""
    assert remove_links_from_markdown(markdown).strip() == expected.strip()

def test_extra_spaces_and_empty_lines():
    # Test collapse of extra spaces
    markdown_spaces = "Too    many    spaces."
    expected_spaces = "Too many spaces."
    assert remove_links_from_markdown(markdown_spaces) == expected_spaces

    # Test collapse of multiple empty lines
    markdown_lines = "Line 1\n\n\n\nLine 2"
    expected_lines = "Line 1\n\nLine 2"
    assert remove_links_from_markdown(markdown_lines) == expected_lines

def test_no_links_or_images():
    markdown = "Just some plain text."
    assert remove_links_from_markdown(markdown) == markdown

def test_empty_string():
    assert remove_links_from_markdown("") == ""
