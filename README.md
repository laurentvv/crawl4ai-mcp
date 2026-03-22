# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](lang/README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](lang/README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](lang/README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](lang/README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](lang/README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](lang/README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](lang/README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](lang/README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](lang/README.id.md)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A powerful web crawling tool that integrates with AI assistants via the MCP (Machine Conversation Protocol). This project allows you to crawl websites and save their content.

## 📋 Features

- Website crawling with configurable depth
- Support for internal and external links
- Generation of structured Markdown files
- Native integration with AI assistants via MCP
- Detailed crawl result statistics
- Error and not found page handling

## 🚀 Installation

### Prerequisites

- [uv](https://github.com/astral-sh/uv)

### Installation Steps

1. Clone this repository:

```bash
git clone https://github.com/laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Install the required dependencies:

```bash
uv sync
```

## 🔧 Configuration

### MCP Configuration for AI Assistants

To use this crawler with AI assistants like VScode Cline, configure your `cline_mcp_settings.json` file:

```json
{
  "mcpServers": {
    "crawl": {
      "command": "uv",
      "args": [
        "run",
        "PATH/TO/YOUR/PROJECT/crawl_mcp.py"
      ],
      "disabled": false,
      "autoApprove": [],
      "timeout": 600
    }
  }
}
```

Replace `PATH/TO/YOUR/PROJECT` with the appropriate path on your system.

## 🖥️ Usage

### Usage with an AI Assistant (via MCP)

Once configured in your AI assistant, you can use the crawler by asking the assistant to perform a crawl using the following syntax:

```
Can you crawl the website https://example.com with a depth of 2?
```

The assistant will use the MCP protocol to run the crawling tool with the specified parameters.

### Usage Examples with Claude

Here are examples of requests you can make to Claude after configuring the MCP tool:

- **Simple Crawl**: "Can you crawl the site example.com and give me a summary?"
- **Crawl with Options**: "Can you crawl https://example.com with a depth of 3 and include external links?"
- **Crawl with Custom Output**: "Can you crawl the blog example.com and save the results in a file named 'blog_analysis.md'?"

## 📁 Result Structure

Crawl results are saved in the `crawl_results` folder at the root of the project. Each result file is in Markdown format with the following structure:

```markdown
# https://example.com/page

## Metadata
- Depth: 1
- Timestamp: 2023-07-01T12:34:56

## Content
Extracted content from the page...

---
```

## 🛠️ Available Parameters

The crawl tool accepts the following parameters:

| Parameter | Type | Description | Default Value |
|-----------|------|-------------|---------------|
| url | string | URL to crawl (required) | - |
| max_depth | integer | Maximum crawling depth | 2 |
| include_external | boolean | Include external links | false |
| verbose | boolean | Enable detailed output | true |
| output_file | string | Output file path | automatically generated |

## 📊 Result Format

The tool returns a summary with:
- URL crawled
- Path to the generated file
- Duration of the crawl
- Statistics about processed pages (successful, failed, not found, access forbidden)

Results are saved in the `crawl_results` directory of your project.

## 🤝 Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
