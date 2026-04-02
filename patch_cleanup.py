import re

with open("src/crawl4ai_mcp/__init__.py", "r") as f:
    content = f.read()

new_remove_links = """def clean_ui_artifacts(text):
    \"\"\"Remove common UI artifacts and empty markdown tags.\"\"\"
    # Common UI strings to remove
    ui_strings = [
        r"(?i)^\\s*Skip to main content\\s*$",
        r"(?i)^\\s*Search\\.\\.\\.\\s*$",
        r"(?i)^\\s*Ctrl K\\s*$",
        r"(?i)^\\s*Copy page\\s*$",
        r"(?i)^\\s*Was this page helpful\\? YesNo\\s*$",
        r"(?i)^\\s*Powered by.*?Mintlify\\s*$"
    ]

    for pattern in ui_strings:
        text = re.sub(pattern, "", text, flags=re.MULTILINE)

    # Remove empty markdown headers like "## "
    # We avoid using actual unicode escape characters in the python source text here
    # to avoid syntax errors in string literals.
    text = re.sub(r'#+\\s*(?:\\n|\\r|\\s)*\\n', '\\n', text)

    # Clean up excessive newlines again
    text = re.sub(r'\\n{3,}', '\\n\\n', text)
    return text

def remove_links_from_markdown(markdown_text):
    \"\"\"
    Remove links and images from markdown text while preserving text and code indentation.
    \"\"\"
    # Identify and protect code blocks
    code_blocks = []

    # Function to replace code blocks with placeholders
    def save_code_block(match):
        code = match.group(0)
        code_blocks.append(code)
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"

    # Identify code blocks (between ``` and ```) and replace them with placeholders
    markdown_with_placeholders = re.sub(r'```[\\s\\S]*?```', save_code_block, markdown_text)

    # Completely remove images in ![text](url) format BEFORE links
    text_without_images = re.sub(r'!\\[[^\\]]*\\]\\([^)]+\\)', '', markdown_with_placeholders)

    # Replace links in [text](url) format with just the text
    text_without_links = re.sub(r'\\[([^\\]]+)\\]\\([^)]+\\)', r'\\1', text_without_images)

    # Clean UI artifacts
    text_cleaned = clean_ui_artifacts(text_without_links)

    # Remove lines containing only spaces
    text_without_empty_lines = re.sub(r'\\n\\s*\\n', '\\n\\n', text_cleaned)

    # Remove blocks of consecutive spaces (but not in code blocks)
    text_without_extra_spaces = re.sub(r' {2,}', ' ', text_without_empty_lines)

    # Put the code blocks back in place
    result = text_without_extra_spaces
    for i, code_block in enumerate(code_blocks):
        result = result.replace(f"__CODE_BLOCK_{i}__", code_block)

    return result"""

# Find the start of remove_links_from_markdown and replace the whole function
start_idx = content.find("def remove_links_from_markdown(markdown_text):")
end_idx = content.find("async def crawl_and_output_to_markdown(")

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_remove_links + "\n\n" + content[end_idx:]

with open("src/crawl4ai_mcp/__init__.py", "w") as f:
    f.write(content)
