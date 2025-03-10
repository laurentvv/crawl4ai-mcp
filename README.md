# Web Crawler MCP

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A powerful web crawling tool that integrates with AI assistants via the MCP (Machine Conversation Protocol). This project allows you to crawl websites and save their content [...]

## 📋 Features

- Website crawling with configurable depth
- Support for internal and external links
- Generation of structured Markdown files
- Native integration with AI assistants via MCP
- Detailed crawl result statistics
- Error and not found page handling

## 🚀 Installation

### Prerequisites

- Python 3.13 or higher
- pip (Python package manager)

### Installation Steps

1. Clone this repository:

```bash
git clone laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Create and activate a virtual environment:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/MacOS
python -m venv .venv
source .venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## 🔧 Configuration

### MCP Configuration for AI Assistants

To use this crawler with AI assistants like VScode Cline, configure your `cline_mcp_settings.json` file:

```json
{
  "mcpServers": {
    "crawl": {
      "command": "PATH\\TO\\YOUR\\ENVIRONMENT\\.venv\\Scripts\\python.exe",
      "args": [
        "PATH\\TO\\YOUR\\PROJECT\\crawl_mcp.py"
      ],
      "disabled": false,
      "autoApprove": [],
      "timeout": 600
    }
  }
}
```

Replace `PATH\\TO\\YOUR\\ENVIRONMENT` and `PATH\\TO\\YOUR\\PROJECT` with the appropriate paths on your system.

#### Concrete Example (Windows)

```json
{
  "mcpServers": {
    "crawl": {
      "command": "C:\\Python\\crawl4ai-mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "D:\\Python\\crawl4ai-mcp\\crawl_mcp.py"
      ],
      "disabled": false,
      "autoApprove": [],
      "timeout": 600
    }
  }
}
```

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

## 🤝 Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.