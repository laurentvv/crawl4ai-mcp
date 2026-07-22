# Web Crawler MCP

<div align="center">
  <img src="https://raw.githubusercontent.com/laurentvv/crawl4ai-mcp-llm/main/assets/banner.svg" alt="Crawl4AI MCP Banner" width="800"/>
</div>

A powerful web crawling tool that integrates with AI assistants via the MCP (Model Context Protocol). This project allows AI assistants to crawl websites, extract dynamic content, navigate through links, and save structured Markdown files directly.

## 📋 Features

- Native integration with AI assistants via MCP
- Return scraped Markdown content directly to the AI
- Extracts and surfaces internal/external links for AI navigation
- Website crawling with configurable depth
- Detailed crawl result statistics
- Error and not found page handling
- **Advanced Scraping Capabilities**:
  - **Magic Mode**: Bypass anti-bots (like Cloudflare) and simulate real browser behavior
  - **Targeted Extraction**: Fetch only what you need using CSS selectors
  - **Custom JavaScript**: Execute code before extraction (clicks, scrolls, form fills)
  - **Persistent Sessions**: Keep cookies and state across requests for authenticated sites
  - **SPA Support**: Wait for dynamic CSS selectors or set explicit pre-extraction delays

## 🚀 MCP Configuration

The simplest and recommended way to use this tool is via `uvx`, which automatically fetches and runs the latest published version from PyPI.

### Prerequisites

- [uv](https://github.com/astral-sh/uv) installed on your system.

### Setup for AI Assistants (e.g., Claude Desktop, Cline)

Add the following to your AI Assistant's MCP configuration file (e.g., `cline_mcp_settings.json` or `claude_desktop_config.json`):

> **Note for Windows Users**: It is highly recommended to specify `--python 3.13` to avoid compilation issues with certain dependencies.

```json
{
  "mcpServers": {
    "crawl": {
      "command": "uvx",
      "args": [
        "--python",
        "3.13",
        "crawl4ai-mcp-llm"
      ],
      "disabled": false,
      "autoApprove": [],
      "timeout": 600
    }
  }
}
```

### Important: Browser Installation

The crawler uses Playwright to handle dynamic content. You must install the required browsers after setting up the tool:

```bash
uv run playwright install chromium
```

## 🖥️ Usage

Once configured, you can use the crawler by asking your AI assistant to perform a crawl.

### Usage Examples with Claude/Cline

- **Simple Crawl**: "Can you crawl the site example.com and give me a summary?"
- **Crawl with Options**: "Can you crawl https://example.com with a depth of 3 and include external links?"
- **Dynamic Content**: "Crawl this React app and wait for the `.main-content` selector to load."
- **Bypass Protections**: "Crawl example.com but use 'magic mode' to bypass the anti-bot protection."
- **Targeted Extraction**: "Crawl the docs site but only extract content matching the `h1, p.lead` CSS selector."

## 🛠️ Available Parameters (MCP Tool)

The `crawl` tool accepts the following parameters:

| Parameter | Type | Description | Default Value |
|-----------|------|-------------|---------------|
| `url` | string | URL to crawl (required) | - |
| `max_depth` | integer | Maximum crawling depth | 2 |
| `include_external` | boolean | Include external links | false |
| `verbose` | boolean | Enable detailed output | true |
| `wait_for_selector` | string | CSS selector to wait for before extracting content. Useful for single-page applications. | None |
| `return_content` | boolean | Whether to return the extracted content directly in the MCP response (truncated to 50k chars if necessary). | true |
| `output_file` | string | Output file path | automatically generated |
| `magic` | boolean | Enable magic mode to bypass anti-bots and simulate a real browser | false |
| `css_selector` | string | Specific CSS selector to extract only targeted elements from the page | None |
| `js_code` | string | Custom JavaScript code to execute on the page before extraction | None |
| `session_id` | string | Persistent session identifier to keep cookies and browser state across requests | None |
| `delay_before_return_html` | number | Delay in seconds to wait before extracting HTML (useful for heavy JS pages) | None |

## 📄 License

This project is licensed under the MIT License.

---

> 🏠 **Source code & documentation**: [github.com/laurentvv/crawl4ai-mcp-llm](https://github.com/laurentvv/crawl4ai-mcp-llm)
