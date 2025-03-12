import io
import os
import re
import sys
import traceback
import urllib.parse
from datetime import datetime

import anyio
import click
import mcp.types as types
from mcp.server.lowlevel import Server

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy

# Configure UTF-8 encoding for all outputs - This code remains useful
# Particularly on Windows where the default encoding may not be UTF-8
# and to ensure consistency in handling international characters
# when crawling multilingual websites
os.environ["PYTHONIOENCODING"] = "utf-8"
# Force UTF-8 usage for stdout/stderr
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

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

    # List of explicit replacements for known problematic characters
    replacements = {
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

    # Apply explicit replacements
    for char, replacement in replacements.items():
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
    # Use a folder in the project instead of temp
    results_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "crawl_results"
    )

    # Create the folder if it doesn't exist
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    return results_dir


async def crawl_website(
    url: str,
    max_depth: int = 2,
    include_external: bool = False,
    verbose: bool = True,
    output_file: str = None,
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
    if not output_file:
        # Use the project folder instead of the temporary folder
        output_file = os.path.join(
            get_results_directory(), generate_filename_from_url(url)
        )

    if verbose:
        print(
            f"Crawling {url} (max depth: {max_depth}, include external: {include_external})",
            file=sys.stderr,
        )
        print(f"Results will be saved to: {output_file}", file=sys.stderr)

    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=max_depth,
            include_external=include_external,
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=verbose,
    )

    result_markdown = io.StringIO()
    stats = {
        "total_pages": 0,
        "successful_pages": 0,
        "failed_pages": 0,
        "not_found_pages": 0,  # 404 pages
        "forbidden_pages": 0,   # New statistic for 403 pages
        "start_time": datetime.now(),
    }

    try:
        async with AsyncWebCrawler(verbose=verbose) as crawler:
            # Add a hook to track progress
            async def progress_callback(event_type, data):
                if event_type == "page_visit_start":
                    stats["total_pages"] += 1
                    if verbose:
                        print(
                            f"[{datetime.now().strftime('%H:%M:%S')}] Visiting: {data['url']} (page {stats['total_pages']})",
                            file=sys.stderr,
                        )
                elif event_type == "page_visit_complete":
                    if data.get("success", False):
                        stats["successful_pages"] += 1
                    else:
                        stats["failed_pages"] += 1

                    if verbose:
                        print(
                            f"[{datetime.now().strftime('%H:%M:%S')}] Completed: {data['url']} (success: {stats['successful_pages']}, failed: {stats['failed_pages']})",
                            file=sys.stderr,
                        )

            # Add the callback to our configuration
            config.progress_callback = progress_callback

            try:
                if verbose:
                    print(
                        f"Starting crawl at {datetime.now().strftime('%H:%M:%S')}",
                        file=sys.stderr,
                    )

                results = await crawler.arun(url, config=config)

                if verbose:
                    print(
                        f"Crawl completed at {datetime.now().strftime('%H:%M:%S')} - {len(results)} pages processed",
                        file=sys.stderr,
                    )
                    print("Generating markdown file...", file=sys.stderr)

                # Ensure that statistics are consistent with the results
                # Count the number of pages with content as successful
                stats["successful_pages"] = 0  # Reset to count correctly
                stats["not_found_pages"] = 0  # Reset the 404 pages counter
                stats["forbidden_pages"] = 0  # Initialize the 403 pages counter

                for idx, result in enumerate(results):
                    try:
                        # Detect 404 pages
                        if hasattr(result, "status_code") and result.status_code == 404:
                            stats["not_found_pages"] += 1
                            if verbose:
                                print(
                                    f"[{datetime.now().strftime('%H:%M:%S')}] Page not found (404): {result.url}",
                                    file=sys.stderr,
                                )
                            continue
                            
                        # Detect 403 pages
                        if hasattr(result, "status_code") and result.status_code == 403:
                            stats["forbidden_pages"] += 1
                            if verbose:
                                print(
                                    f"[{datetime.now().strftime('%H:%M:%S')}] Access forbidden (403): {result.url}",
                                    file=sys.stderr,
                                )
                            continue

                        text_for_output = getattr(result, "markdown", None) or getattr(
                            result, "text", None
                        )

                        # Check if the content looks like a 404 page (contains "404 Not Found")
                        if text_for_output and "404 Not Found" in text_for_output:
                            stats["not_found_pages"] += 1
                            if verbose:
                                print(
                                    f"[{datetime.now().strftime('%H:%M:%S')}] Page not found (content 404): {result.url}",
                                    file=sys.stderr,
                                )
                            continue
                            
                        # Check if the content looks like a 403 page (contains "403 Forbidden")
                        if text_for_output and "403 Forbidden" in text_for_output:
                            stats["forbidden_pages"] += 1
                            if verbose:
                                print(
                                    f"[{datetime.now().strftime('%H:%M:%S')}] Access forbidden (content 403): {result.url}",
                                    file=sys.stderr,
                                )
                            continue

                        if not text_for_output:
                            continue

                        # Increment the successful pages counter
                        stats["successful_pages"] += 1

                        # Sanitize all elements that will be written
                        safe_url = sanitize_text(result.url)
                        safe_depth = sanitize_text(
                            str(result.metadata.get("depth", "N/A"))
                        )
                        safe_timestamp = sanitize_text(datetime.now().isoformat())
                        safe_content = sanitize_text(text_for_output)

                        md_content = f"""
# {safe_url}

## Metadata
- Depth: {safe_depth}
- Timestamp: {safe_timestamp}

## Content
{safe_content}

---
"""
                        result_markdown.write(md_content)
                    except Exception as e:
                        print(
                            f"Error processing result {idx}: {e}",
                            file=sys.stderr,
                        )
                        # Log problematic content for diagnosis
                        if verbose:
                            print(
                                f"Possible problematic characters in: {result.url}",
                                file=sys.stderr,
                            )
            except Exception as e:
                print(f"Error during crawling execution: {e}", file=sys.stderr)
                return {
                    "error": f"Crawling error: {str(e)}",
                    "file_path": None,
                    "stats": stats,
                }
    except Exception as e:
        print(f"Error initializing crawler: {e}", file=sys.stderr)
        return {
            "error": f"Initialization error: {str(e)}",
            "file_path": None,
            "stats": stats,
        }

    # Write content to the specified file
    try:
        content = result_markdown.getvalue()

        if verbose:
            print(
                f"Writing results to file: {output_file}",
                file=sys.stderr,
            )

        # Create parent directory if needed
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

        # Sanitize and write content
        with open(output_file, "w", encoding="utf-8", errors="replace") as f:
            safe_content = sanitize_text(content)
            f.write(safe_content)

        # Finalize stats
        stats["end_time"] = datetime.now()
        stats["duration_seconds"] = (
            stats["end_time"] - stats["start_time"]
        ).total_seconds()

        if verbose:
            print(
                f"Crawl completed in {stats['duration_seconds']:.2f} seconds",
                file=sys.stderr,
            )
            print(
                f"Pages processed: {stats['successful_pages']} successful, {stats['failed_pages']} failed, "
                f"{stats['not_found_pages']} not found (404), {stats['forbidden_pages']} access forbidden (403)",
                file=sys.stderr,
            )
            print(f"Results saved to: {output_file}", sys.stderr)

        return {"file_path": output_file, "stats": stats, "error": None}
    except Exception as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return {
            "error": f"Writing error: {str(e)}",
            "file_path": None,
            "stats": stats,
        }


@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(port: int, transport: str) -> int:
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

        try:
            result = await crawl_website(
                arguments["url"],
                max_depth=max_depth,
                include_external=include_external,
                verbose=verbose,
                output_file=output_file,
            )

            if result["error"]:
                return [
                    types.TextContent(type="text", text=f"Error: {result['error']}")
                ]

            file_path = result["file_path"]
            stats = result["stats"]

            # Create a summary message
            summary = f"""
## Crawl completed successfully
- URL: {arguments["url"]}
- Result file: {file_path}
- Duration: {stats["duration_seconds"]:.2f} seconds
- Pages processed: {stats["successful_pages"]} successful, {stats["failed_pages"]} failed, 
  {stats.get("not_found_pages", 0)} not found (404), {stats.get("forbidden_pages", 0)} access forbidden (403)

You can view the results in the file: {file_path}
(Results are now stored in the 'crawl_results' folder of your project)
            """

            return [types.TextContent(type="text", text=summary)]
        except Exception as e:
            print(f"Error in crawl_tool: {e}", file=sys.stderr)
            print(traceback.format_exc(), sys.stderr)
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
                    },
                },
            )
        ]

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route

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

        import uvicorn

        uvicorn.run(starlette_app, host="127.0.0.1", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Main error: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)