import pytest
from crawl4ai_mcp import sanitize_text
import sys
from unittest.mock import patch

def test_sanitize_text_none():
    """Test sanitize_text with None input."""
    assert sanitize_text(None) == ""

def test_sanitize_text_string():
    """Test sanitize_text with standard string input."""
    assert sanitize_text("hello world") == "hello world"

def test_sanitize_text_replacements():
    """Test sanitize_text with characters that need replacement."""
    # Test replacements documented in the function
    text = "Arrow →, Quote ‘, Space \u00a0"

    # We must mock sys.getdefaultencoding to 'ascii' to trigger the UnicodeEncodeError
    # since in 'utf-8', these characters can be encoded without error.
    with patch("sys.getdefaultencoding", return_value="ascii"):
        assert sanitize_text(text) == "Arrow ->, Quote ', Space  "

def test_sanitize_text_non_string():
    """Test sanitize_text with non-string input (like int or float)."""
    assert sanitize_text(123) == "123"
