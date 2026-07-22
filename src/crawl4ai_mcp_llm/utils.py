import os
import re
import sys
import urllib.parse
import uuid
from datetime import datetime

# Pre-compiled UI artifact regex
UI_ARTIFACTS_REGEX = re.compile(
    r"(?i)^\s*(?:Skip to main content|Search\.\.\.|Ctrl K|Copy page|Was this page helpful\? YesNo|Powered by.*?Mintlify)\s*$",
    flags=re.MULTILINE
)

# Pre-compiled regex patterns for markdown cleaning
EMPTY_HEADERS_REGEX = re.compile(r'#+\s*(?:\n|\r|\s)*\n')
EXCESSIVE_NEWLINES_REGEX = re.compile(r'\n{3,}')
CODE_BLOCK_REGEX = re.compile(r'```[\s\S]*?```')
IMAGE_REGEX = re.compile(r'!\[[^\]]*\]\([^)]+\)')
LINK_REGEX = re.compile(r'\[([^\]]+)\]\([^)]+\)')
EMPTY_LINES_REGEX = re.compile(r'\n\s*\n')
EXTRA_SPACES_REGEX = re.compile(r' {2,}')

UNICODE_REPLACEMENTS = {
    "\u2192": "->",  # Right arrow → becomes ->
    "\u2190": "<-",  # Left arrow ← becomes <-
    "\u2191": "^",   # Up arrow ↑ becomes ^
    "\u2193": "v",   # Down arrow ↓ becomes v
    "\u2022": "*",   # Bullet • becomes *
    "\u2013": "-",   # En dash – becomes -
    "\u2014": "--",  # Em dash — becomes --
    "\u2018": "'",   # Left single quotation mark ' becomes '
    "\u2019": "'",   # Right single quotation mark ' becomes '
    "\u201c": '"',   # Left double quotation mark " becomes "
    "\u201d": '"',   # Right double quotation mark " becomes "
    "\u2026": "...", # Ellipsis … becomes ...
    "\u00a0": " ",   # Non-breaking space   becomes normal space
}

def sanitize_text(text):
    """
    Sanitize the input text by replacing known problematic characters with their
    ASCII equivalents and removing any other non-ASCII characters.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)

    if text.isascii():
        return text

    try:
        # Test if the text can be encoded in the default system encoding
        text.encode(sys.getdefaultencoding())
    except UnicodeEncodeError:
        # If it can't, replace problematic characters
        # Apply explicit replacements
        for char, replacement in UNICODE_REPLACEMENTS.items():
            if char in text:
                text = text.replace(char, replacement)

        # Eliminate all other non-ASCII characters that might cause problems
        if not text.isascii():
            text = re.sub(r"[^\x00-\x7F]+", " ", text)

    return text

def generate_filename_from_url(url):
    """Generates a valid filename from a URL"""
    # Extract hostname and path
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.netloc.replace(".", "_")

    # Add a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create the filename
    return f"crawl_{hostname}_{timestamp}.md"


def get_results_directory():
    """Returns the path to the directory for storing results"""
    env_dir = os.getenv("CRAWL4AI_RESULTS_DIR")
    if env_dir:
        results_dir = os.path.abspath(env_dir)
    else:
        results_dir = os.path.expanduser("~/.crawl4ai_mcp_llm/results")

    # Create the folder if it doesn't exist
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    return results_dir

def is_safe_path(path, base_dir):
    """Checks if a path is safe (i.e., within the base directory)"""
    # Use realpath to resolve any symlinks and .. components
    abs_path = os.path.realpath(path)
    abs_base = os.path.realpath(base_dir)

    # Check if abs_path is within abs_base
    return os.path.commonpath([abs_path, abs_base]) == abs_base

def clean_ui_artifacts(text):
    """Remove common UI artifacts and empty markdown tags."""
    text = UI_ARTIFACTS_REGEX.sub("", text)

    # Remove empty markdown headers like "## "
    text = EMPTY_HEADERS_REGEX.sub('\n', text)

    # Clean up excessive newlines again
    text = EXCESSIVE_NEWLINES_REGEX.sub('\n\n', text)
    return text

def remove_links_from_markdown(markdown_text):
    """
    Remove links and images from markdown text while preserving text and code indentation.
    """
    # Identify and protect code blocks
    code_blocks = []
    
    # Generate a unique prefix for this run
    block_prefix = f"__CODE_BLOCK_{uuid.uuid4().hex}_"
    
    # Function to replace code blocks with placeholders
    def save_code_block(match):
        code = match.group(0)
        code_blocks.append(code)
        return f"{block_prefix}{len(code_blocks)-1}__"
    
    # Identify code blocks (between ``` and ```) and replace them with placeholders
    markdown_with_placeholders = CODE_BLOCK_REGEX.sub(save_code_block, markdown_text)
    
    # Completely remove images in ![text](url) format BEFORE links
    text_without_images = IMAGE_REGEX.sub('', markdown_with_placeholders)

    # Replace links in [text](url) format with just the text
    text_without_links = LINK_REGEX.sub(r'\1', text_without_images)
    
    # Clean UI artifacts
    text_cleaned = clean_ui_artifacts(text_without_links)
    
    # Remove lines containing only spaces
    text_without_empty_lines = EMPTY_LINES_REGEX.sub('\n\n', text_cleaned)
    
    # Remove blocks of consecutive spaces (but not in code blocks)
    text_without_extra_spaces = EXTRA_SPACES_REGEX.sub(' ', text_without_empty_lines)
    
    # Put the code blocks back in place
    restore_regex = re.compile(f'{block_prefix}(\\d+)__')
    def restore_code_block(match):
        index = int(match.group(1))
        return code_blocks[index]

    result = restore_regex.sub(restore_code_block, text_without_extra_spaces)
    
    return result
