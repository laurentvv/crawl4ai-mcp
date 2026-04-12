import unittest
from unittest.mock import MagicMock
import sys

# Local mock of dependencies for importing the module under test
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

setup_mocks()

# Ensure src is in path
if "src" not in sys.path:
    sys.path.insert(0, "src")

from crawl4ai_mcp import clean_ui_artifacts

class TestCleanUIArtifacts(unittest.TestCase):
    """
    Test suite for the clean_ui_artifacts function.
    """

    def test_remove_ui_strings(self):
        """Test removal of common UI artifacts."""
        test_cases = [
            ("Skip to main content", ""),
            ("  Search...  ", ""),
            ("ctrl k", ""),
            ("Copy page", ""),
            ("Was this page helpful? YesNo", ""),
            ("Powered by Mintlify", ""),
            # "Keep this text\nSkip to main content\nKeep this too"
            # should become "Keep this text\n\nKeep this too" (if removal leaves an empty line)
        ]
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(clean_ui_artifacts(input_text).strip(), expected.strip())

    def test_remove_empty_headers(self):
        """Test removal of empty markdown headers."""
        test_cases = [
            ("# \n", "\n"),
            ("## \r\n", "\n"),
            ("###    \n", "\n"),
            ("#### \nMore text", "\nMore text"),
            ("# Header with text\n", "# Header with text\n"),
        ]
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(clean_ui_artifacts(input_text), expected)

    def test_collapse_newlines(self):
        """Test collapsing of 3+ consecutive newlines."""
        test_cases = [
            ("Text\n\n\nMore text", "Text\n\nMore text"),
            ("Text\n\n\n\n\nMore text", "Text\n\nMore text"),
            ("Text\n\nMore text", "Text\n\nMore text"),
        ]
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(clean_ui_artifacts(input_text), expected)

    def test_preserve_content(self):
        """Test that legitimate content is preserved."""
        content = """
# Real Header
This is a paragraph.
- List item 1
- List item 2

```python
def hello():
    print("world")
```

Another paragraph.
"""
        self.assertEqual(clean_ui_artifacts(content), content)

    def test_combined_artifacts(self):
        """Test a mix of artifacts and content."""
        input_text = """#
Skip to main content
## Real Header


Search...


Text here.


"""
        # Manual trace of the function:
        # Original:
        # "# \nSkip to main content\n## Real Header\n\n\nSearch...\n\n\nText here.\n\n\n"

        # 1. re.sub("(?i)^\s*Skip to main content\s*$", "", ..., flags=re.MULTILINE)
        # Result: "# \n\n## Real Header\n\n\nSearch...\n\n\nText here.\n\n\n" (note the double newline)

        # 2. re.sub("(?i)^\s*Search\.\.\.\s*$", "", ..., flags=re.MULTILINE)
        # Result: "# \n\n## Real Header\n\n\n\n\n\nText here.\n\n\n"

        # 3. re.sub(r'#+\s*(?:\n|\r|\s)*\n', '\n', text)
        # This matches "# \n\n" ?
        # Match: #+ (\s* \n \n) matches!
        # Result: "\n## Real Header\n\n\n\n\n\nText here.\n\n\n"

        # 4. re.sub(r'\n{3,}', '\n\n', text)
        # Match: \n\n\n\n\n\n -> \n\n
        # Result: "\n## Real Header\n\nText here.\n\n"

        expected = "\n## Real Header\n\nText here.\n\n"
        self.assertEqual(clean_ui_artifacts(input_text), expected)

if __name__ == "__main__":
    unittest.main()
