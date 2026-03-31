import io
import os
import re
import sys
import traceback
import urllib.parse
from datetime import datetime

import anyio
import click
import uvicorn
import mcp.types as types
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from mcp.server.lowlevel import Server
from mcp.server.sse import SseServerTransport
from mcp.server.stdio import stdio_server
from starlette.applications import Starlette
from starlette.routing import Mount, Route

os.environ["PYTHONIOENCODING"] = "utf-8"
# Force UTF-8 usage for stdout/stderr
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

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



# Improved function to sanitize texts with explicit replacement of problematic characters
def sanitize_text(text):
    """
    Sanitize the input text by replacing known problematic characters with their
    ASCII equivalents and removing any other non-ASCII characters.
    Args:
        text (str): The input text to be sanitized. If None, an empty string is returned.
    Returns:
        str: The sanitized text with problematic characters replaced and non-ASCII
             characters removed.
    Replacements:
        - Right arrow (→) becomes "->"
        - Left arrow (←) becomes "<-"
        - Up arrow (↑) becomes "^"
        - Down arrow (↓) becomes "v"
        - Bullet (•) becomes "*"
        - En dash (–) becomes "-"
        - Em dash (—) becomes "--"
        - Left single quotation mark (‘) becomes "'"
        - Right single quotation mark (’) becomes "'"
        - Left double quotation mark (“) becomes '"'
        - Right double quotation mark (”) becomes '"'
        - Ellipsis (…) becomes "..."
        - Non-breaking space ( ) becomes a normal space
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)

    try:
        # Test if the text can be encoded in the default system encoding
        text.encode(sys.getdefaultencoding())
    except UnicodeEncodeError:
        # If it can't, replace problematic characters
        # Apply explicit replacements
        for char, replacement in UNICODE_REPLACEMENTS.items():
            text = text.replace(char, replacement)

        # Eliminate all other non-ASCII characters that might cause problems
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
    # Use the current working directory (os.getcwd()) to store results in the user's project
    # instead of the package installation directory (e.g., in a uv cache)
    results_dir = os.path.join(os.getcwd(), "crawl_results")

    # Create the folder if it doesn't exist
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    return results_dir


def is_safe_path(path, base_dir):
    """
    Checks if the path is safe (i.e., it is within the base_dir).
    Args:
        path (str): The path to check.
        base_dir (str): The base directory.
    Returns:
        bool: True if the path is safe, False otherwise.
    """
    abs_base = os.path.realpath(base_dir)
    abs_path = os.path.realpath(path)
    # Ensure the path starts with the base directory and handles directory separators correctly
    return abs_path.startswith(abs_base + os.sep) or abs_path == abs_base


def remove_links_from_markdown(markdown_text):
    """
    Remove links and images from markdown text while preserving text and code indentation.
    
    Args:
        markdown_text (str): The markdown text to be processed
        
    Returns:
        str: Markdown text with links and images removed
    """
    # Identify and protect code blocks
    code_blocks = []
    
    # Function to replace code blocks with placeholders
    def save_code_block(match):
        code = match.group(0)
        code_blocks.append(code)
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"
    
    # Identify code blocks (between ``` and ```) and replace them with placeholders
    markdown_with_placeholders = re.sub(r'```[\s\S]*?```', save_code_block, markdown_text)
    
    # Replace links in [text](url) format with just the text
    text_without_links = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', markdown_with_placeholders)
    
    # Completely remove images in ![text](url) format
    text_without_images = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', text_without_links)
    
    # Remove lines containing only spaces
    text_without_empty_lines = re.sub(r'\n\s*\n', '\n\n', text_without_images)
    
    # Remove blocks of consecutive spaces (but not in code blocks)
    text_without_extra_spaces = re.sub(r' {2,}', ' ', text_without_empty_lines)
    
    # Put the code blocks back in place
    result = text_without_extra_spaces
    for i, code_block in enumerate(code_blocks):
        result = result.replace(f"__CODE_BLOCK_{i}__", code_block)
    
    return result

async def crawl_and_output_to_markdown(start_url: str,
    max_depth: int = 5,
    include_external: bool = False,
    verbose: bool = True,
    output_file: str = None,
    wait_for_selector: str = None,
) -> dict:
    """
    Crawl a website and save the results to a file

    Args:
        url: URL to crawl
        max_depth: Maximum crawl depth
        include_external: Include external links
        verbose: Display detailed information
        output_file: Output file path (automatically generated if None)

    Returns:
        A dictionary containing the file path and statistics
    """
    # Generate a filename if not specified
    results_dir = get_results_directory()
    if not output_file:
        # Use the project folder instead of the temporary folder
        output_file = os.path.join(results_dir, generate_filename_from_url(start_url))
    else:
        # Validate that the output file path is safe (doesn't escape the results directory)
        if not is_safe_path(output_file, results_dir):
            raise ValueError(f"Unsafe output file path: {output_file}. Paths must be within the 'crawl_results' directory.")

    # Set basic configuration
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=max_depth,
            include_external=include_external,
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=verbose,
    )

    if wait_for_selector:
        config.wait_for = wait_for_selector

    try:
        async with AsyncWebCrawler() as crawler:
            results = await crawler.arun(start_url, config=config)
            print(f"Crawled {len(results)} pages in total")
            
            # Create the parent folder if necessary
            await anyio.Path(os.path.dirname(os.path.abspath(output_file))).mkdir(parents=True, exist_ok=True)
            
            # Call results_to_markdown and get the result
            return await results_to_markdown(results, output_file)
    except Exception as e:
        print(f"Error during crawling: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return {
            "error": f"Crawling error: {str(e)}",
            "file_path": None,
            "stats": {
                "successful_pages": 0,
                "failed_pages": 0,
                "not_found_pages": 0,
                "forbidden_pages": 0,
                "duration_seconds": 0
            }
        }


def _extract_page_content_and_errors(result) -> tuple[str | None, str | None]:
    """
    Extract text content from a result and check for common HTTP errors.
    Returns a tuple of (content, error_type) where error_type is '404', '403', or 'missing'.
    """
    text_for_output = getattr(result, "markdown", None) or getattr(result, "text", None)
    if not text_for_output:
        return None, "missing"

    # Check if it's an error page (404 or 403)
    if ("404 Not Found" in text_for_output or "403 Forbidden" in text_for_output) and "nginx" in text_for_output:
        error_type = "404" if "404 Not Found" in text_for_output else "403"
        return text_for_output, error_type

    # Check metadata title for error indicators
    title = result.metadata.get("title", "Untitled page") if hasattr(result, "metadata") else "Untitled page"
    error_indicators = ["404", "403", "Not Found", "Forbidden"]
    if any(indicator in title for indicator in error_indicators):
        error_type = "404" if "404" in title or "Not Found" in title else "403"
        # We still want to use the text but note it's an error
        return text_for_output, error_type

    return text_for_output, None

def _format_markdown_page(result, text_for_output: str) -> str:
    """
    Format a single crawl result into a Markdown string.
    """
    # Remove links from Markdown text
    clean_text = remove_links_from_markdown(text_for_output)

    # Structuring metadata
    metadata = {
        "depth": result.metadata.get("depth", "N/A") if hasattr(result, "metadata") else "N/A",
        "timestamp": datetime.now().isoformat(),
        "title": result.metadata.get("title", "Untitled page") if hasattr(result, "metadata") else "Untitled page",
    }

    # Formatted writing with literal template
    return f"""
# {metadata["title"]}

## URL
{result.url}

## Metadata
- Depth: {metadata["depth"]}
- Timestamp: {metadata["timestamp"]}

## Content
{clean_text}

---
"""

def _extract_unique_links(results: list) -> dict:
    """
    Extract and deduplicate internal and external links from crawl results.
    """
    links = {"internal": [], "external": []}
    seen_hrefs = {"internal": set(), "external": set()}

    for result in results:
        if hasattr(result, "links") and isinstance(result.links, dict):
            for k in ["internal", "external"]:
                if k in result.links:
                    for link in result.links[k]:
                        # avoid duplicates based on href
                        href = link.get('href')
                        if href and href not in seen_hrefs[k]:
                            links[k].append(link)
                            seen_hrefs[k].add(href)

    return links

async def results_to_markdown(results: list, output_path: str) -> dict:
    """
    Convert crawl results to a markdown file
    
    Args:
        results: List of crawl results
        output_path: Output file path
        
    Returns:
        A dictionary containing statistics and operation status
    """
    stats = {
        "successful_pages": 0,
        "failed_pages": 0,
        "not_found_pages": 0,
        "forbidden_pages": 0,
        "start_time": datetime.now()
    }
    
    try:
        async with await anyio.Path(output_path).open("w", encoding="utf-8") as md_file:
            for result in results:
                text_for_output, error_type = _extract_page_content_and_errors(result)

                if error_type == "missing":
                    print(f"No content found for {result.url} - Skipped")
                    stats["failed_pages"] += 1
                    continue
                elif error_type in ("404", "403"):
                    # For title errors, original code prints slightly differently
                    title = result.metadata.get("title", "Untitled page") if hasattr(result, "metadata") else "Untitled page"
                    error_indicators = ["404", "403", "Not Found", "Forbidden"]
                    
                    if any(indicator in title for indicator in error_indicators):
                        print(f"Page with error title detected and skipped: {result.url}")
                    else:
                        print(f"{error_type} page detected and skipped: {result.url}")

                    if error_type == "404":
                        stats["not_found_pages"] += 1
                    else:
                        stats["forbidden_pages"] += 1
                    continue

                md_content = _format_markdown_page(result, text_for_output)
                await md_file.write(md_content)
                stats["successful_pages"] += 1
            
            # Display a summary at the end
            print(f"Valid pages processed: {stats['successful_pages']}")
            print(f"Error pages (403/404) skipped: {stats['not_found_pages'] + stats['forbidden_pages']}")
        
        links = _extract_unique_links(results)

        # Finalize statistics
        stats["end_time"] = datetime.now()
        stats["duration_seconds"] = (stats["end_time"] - stats["start_time"]).total_seconds()
        
        return {
            "file_path": output_path,
            "stats": stats,
            "links": links,
            "error": None
        }
    
    except Exception as e:
        print(f"Error writing markdown file: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return {
            "error": f"Writing error: {str(e)}",
            "file_path": None,
            "stats": stats
        }

app = Server("mcp-web-crawler")

@app.call_tool()
async def crawl_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name != "crawl":
        raise ValueError(f"Unknown tool: {name}")
    if "url" not in arguments:
        raise ValueError("Missing required argument 'url'")

    max_depth = arguments.get("max_depth", 2)
    include_external = arguments.get("include_external", False)
    verbose = arguments.get("verbose", True)
    output_file = arguments.get("output_file", None)
    wait_for_selector = arguments.get("wait_for_selector", None)
    return_content = arguments.get("return_content", True)

    try:
        result = await crawl_and_output_to_markdown(
            arguments["url"],
            max_depth=max_depth,
            include_external=include_external,
            verbose=verbose,
            output_file=output_file,
            wait_for_selector=wait_for_selector,
        )

        if result["error"]:
            return [
                types.TextContent(type="text", text=f"Error: {result['error']}")
            ]

        file_path = result["file_path"]
        stats = result["stats"]

        links_summary = ""
        if "links" in result:
            internal_links = [link.get("href") for link in result["links"].get("internal", [])[:20]]
            external_links = [link.get("href") for link in result["links"].get("external", [])[:20]]
            if internal_links or external_links:
                links_summary = "\n## Extracted Links (Sample)"
                if internal_links:
                    links_summary += "\n### Internal Links\n- " + "\n- ".join(internal_links)
                if external_links:
                    links_summary += "\n### External Links\n- " + "\n- ".join(external_links)
                links_summary += "\n"

        content_text = ""
        if return_content and file_path:
            try:
                async with await anyio.Path(file_path).open("r", encoding="utf-8") as f:
                    content_text = await f.read()

                max_chars = 50000
                if len(content_text) > max_chars:
                    content_text = content_text[:max_chars] + "\n\n...[Content truncated due to length]..."

                content_text = f"\n\n## Extracted Content\n\n{content_text}"
            except Exception as e:
                print(f"Failed to read content for return: {e}")

        summary = f"""
## Crawl completed successfully
- URL: {arguments["url"]}
- Result file: {file_path}
- Duration: {stats["duration_seconds"]:.2f} seconds
- Pages processed: {stats["successful_pages"]} successful, {stats["failed_pages"]} failed, 
  {stats.get("not_found_pages", 0)} not found (404), {stats.get("forbidden_pages", 0)} access forbidden (403)
{links_summary}
You can view the full results in the file: {file_path}
(Results are now stored in the 'crawl_results' folder of your project)
{content_text}
        """
        return [types.TextContent(type="text", text=summary)]
    except Exception as e:
        print(f"Error in crawl_tool: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return [
            types.TextContent(type="text", text=f"Error: {sanitize_text(str(e))}")
        ]

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="crawl",
            description="Crawls a website and saves its content as structured markdown to a file",
            inputSchema={
                "type": "object",
                "required": ["url"],
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to crawl",
                    },
                    "max_depth": {
                        "type": "integer",
                        "description": "Maximum crawling depth",
                        "default": 2,
                    },
                    "include_external": {
                        "type": "boolean",
                        "description": "Whether to include external links",
                        "default": False,
                    },
                    "verbose": {
                        "type": "boolean",
                        "description": "Enable verbose output",
                        "default": True,
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Path to output file (generated if not provided)",
                        "default": None,
                    },
                    "wait_for_selector": {
                        "type": "string",
                        "description": "CSS selector to wait for before extracting content. Useful for single-page applications.",
                        "default": None,
                    },
                    "return_content": {
                        "type": "boolean",
                        "description": "Whether to return the extracted content directly in the MCP response",
                        "default": True,
                    },
                },
            },
        )
    ]

def run_sse_server(app: Server, port: int):
    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request.send
        ) as streams:
            await app.run(
                streams[0], streams[1], app.create_initialization_options()
            )

    starlette_app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

    uvicorn.run(starlette_app, host="127.0.0.1", port=port)

def run_stdio_server(app: Server):
    async def arun():
        async with stdio_server() as streams:
            await app.run(
                streams[0], streams[1], app.create_initialization_options()
            )

    anyio.run(arun)

@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(port: int, transport: str) -> int:
    if transport == "sse":
        run_sse_server(app, port)
    else:
        run_stdio_server(app)
    return 0

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Main error: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)
