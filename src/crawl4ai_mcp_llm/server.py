import sys
import traceback
import anyio
import mcp.types as types
from mcp.server.lowlevel import Server

from .crawler import crawl_and_output_to_markdown, CRAWL4AI_MCP_ALLOW_JS_ENV
from .utils import sanitize_text

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
    magic = arguments.get("magic", False)
    css_selector = arguments.get("css_selector", None)
    js_code = arguments.get("js_code", None)
    session_id = arguments.get("session_id", None)
    delay_before_return_html = arguments.get("delay_before_return_html", None)

    try:
        result = await crawl_and_output_to_markdown(
            arguments["url"],
            max_depth=max_depth,
            include_external=include_external,
            verbose=verbose,
            output_file=output_file,
            wait_for_selector=wait_for_selector,
            magic=magic,
            css_selector=css_selector,
            js_code=js_code,
            session_id=session_id,
            delay_before_return_html=delay_before_return_html,
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
            description=(
                "Crawls a website and saves its content as structured markdown to a file.\n\n"
                "⚠️ PERFORMANCE WARNING: This tool can take from 30 seconds to several minutes "
                "depending on the site. Heavy/SPA sites (React, Next.js, Mintlify), high "
                "`max_depth`, and the first crawl of a session (Playwright browser startup) "
                "are especially slow. The MCP client timeout should be set generously "
                "(e.g. 600000 ms / 10 min).\n\n"
                "TIPS to speed up crawls:\n"
                "- Use `css_selector` to extract only the relevant content (e.g. 'main', 'article').\n"
                "- Use `wait_for_selector` for single-page applications.\n"
                "- Lower `max_depth` (1 = single page) when you don't need recursive crawling.\n"
                "- Warn the user before launching a crawl that it may take a while."
            ),
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
                    },
                    "wait_for_selector": {
                        "type": "string",
                        "description": "CSS selector to wait for before extracting content. Useful for single-page applications.",
                    },
                    "return_content": {
                        "type": "boolean",
                        "description": "Whether to return the extracted content directly in the MCP response",
                        "default": True,
                    },
                    "magic": {
                        "type": "boolean",
                        "description": "Enable magic mode to bypass anti-bots and simulate a real browser",
                        "default": False,
                    },
                    "css_selector": {
                        "type": "string",
                        "description": "Specific CSS selector to extract only targeted elements from the page",
                    },
                    "js_code": {
                        "type": "string",
                        "description": f"Custom JavaScript code to execute on the page before extraction (Requires {CRAWL4AI_MCP_ALLOW_JS_ENV}=true environment variable)",
                    },
                    "session_id": {
                        "type": "string",
                        "description": "Persistent session identifier to keep cookies and browser state across requests",
                    },
                    "delay_before_return_html": {
                        "type": "number",
                        "description": "Delay in seconds to wait before extracting HTML (useful for heavy JS pages)",
                    },
                },
            },
        )
    ]
