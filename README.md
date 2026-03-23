# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](lang/README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](lang/README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](lang/README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](lang/README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](lang/README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](lang/README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](lang/README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](lang/README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](lang/README.id.md)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A powerful web crawling tool that integrates with AI assistants via the MCP (Model Context Protocol). This project allows AI assistants to crawl websites, extract dynamic content, navigate through links, and save structured Markdown files directly.

## 📋 Features

- Native integration with AI assistants via MCP
- Return scraped Markdown content directly to the AI
- Extracts and surfaces internal/external links for AI navigation
- Wait for dynamic CSS selectors before scraping (SPA support)
- Website crawling with configurable depth
- Detailed crawl result statistics
- Error and not found page handling

## 🚀 MCP Configuration

The simplest and recommended way to use this tool is via `uvx`, which automatically fetches and runs the latest version from GitHub without requiring you to clone the repository manually.

### Prerequisites

- [uv](https://github.com/astral-sh/uv) installed on your system.

### Setup for AI Assistants (e.g., Claude Desktop, Cline)

Add the following to your AI Assistant's MCP configuration file (e.g., `cline_mcp_settings.json` or `claude_desktop_config.json`):

> **Note for Windows Users**: It is highly recommended to specify `--python 3.12` to avoid compilation issues with certain dependencies.

```json
{
  "mcpServers": {
    "crawl": {
      "command": "uvx",
      "args": [
        "--python",
        "3.12",
        "--from",
        "git+https://github.com/laurentvv/crawl4ai-mcp",
        "crawl4ai-mcp"
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

## 👨‍💻 Development

If you want to modify the crawler or run it locally:

1. Clone this repository:
```bash
git clone https://github.com/laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Install dependencies using `uv`:
```bash
uv sync
```

3. Run the MCP server directly:
```bash
uv run crawl4ai-mcp
```

## 🤝 Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
