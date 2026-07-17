# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.13%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

<div align="center">
  <img src="../assets/banner.jpg" alt="Crawl4AI MCP Banner" width="800"/>
</div>

一个强大的网络爬虫工具，通过 MCP（模型上下文协议）与 AI 助手集成。该项目允许 AI 助手抓取网站、提取动态内容、通过链接导航并直接保存结构化的 Markdown 文件。

## 📋 功能特点

- 通过 MCP 与 AI 助手进行原生集成
- 直接向 AI 返回抓取的 Markdown 内容
- 提取并显示内部/外部链接，供 AI 导航
- 可配置深度的网站抓取
- 详细的抓取结果统计
- 错误和页面未找到处理
- **高级抓取功能**：
  - **魔法模式 (Magic Mode)**：绕过反机器人验证（如 Cloudflare）并模拟真实的浏览器行为
  - **定向提取**：使用 CSS 选择器仅获取您需要的内容
  - **自定义 JavaScript**：在提取之前执行代码（点击、滚动、表单填写）
  - **持久化会话**：在已验证的网站上保持跨请求的 Cookie 和浏览器状态
  - **单页面应用 (SPA) 支持**：等待动态 CSS 选择器或设置明确的提取前延迟

## 🚀 MCP 配置

使用此工具最简单且推荐的方法是通过 `uvx`，它会自动从 GitHub 获取并运行最新版本，无需手动克隆仓库。

### 前提条件

- 系统中已安装 [uv](https://github.com/astral-sh/uv)。

### AI 助手设置（例如 Claude Desktop, Cline）

将以下内容添加到 AI 助手的 MCP 配置文件中（例如 `cline_mcp_settings.json` 或 `claude_desktop_config.json`）：

> **Windows 用户注意**：强烈建议指定 `--python 3.13`，以避免某些依赖项的编译问题。

```json
{
  "mcpServers": {
    "crawl": {
      "command": "uvx",
      "args": [
        "--python",
        "3.13",
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

### 重要提示：浏览器安装

该爬虫使用 Playwright 处理动态内容。设置工具后，您必须安装所需的浏览器：

```bash
uv run playwright install chromium
```

## 🖥️ 使用方法

配置完成后，您可以通过要求 AI 助手执行抓取来使用爬虫。

### Claude/Cline 使用示例

- **简单抓取**：“你能抓取 example.com 网站并给我一个总结吗？”
- **带选项的抓取**：“你能抓取 https://example.com，深度为 3 并包含外部链接吗？”
- **动态内容**：“抓取这个 React 应用并等待 `.main-content` 选择器加载。”
- **绕过保护**：“抓取 example.com，但使用‘魔法模式’以绕过反机器人保护。”
- **定向提取**：“抓取文档网站，但仅提取与 `h1, p.lead` CSS 选择器匹配的内容。”

## 🛠️ 可用参数 (MCP 工具)

`crawl` 工具接受以下参数：

| 参数 | 类型 | 描述 | 默认值 |
|-----------|------|-------------|---------------|
| `url` | string | 要抓取的 URL（必填） | - |
| `max_depth` | integer | 最大抓取深度 | 2 |
| `include_external` | boolean | 包含外部链接 | false |
| `verbose` | boolean | 启用详细输出 | true |
| `wait_for_selector` | string | 提取内容前等待的 CSS 选择器。适用于单页面应用 (SPA)。 | None |
| `return_content` | boolean | 是否直接在 MCP 响应中返回提取的内容（必要时截断至 50k 字符）。 | true |
| `output_file` | string | 输出文件路径 | 自动生成 |
| `magic` | boolean | 启用魔法模式以绕过反机器人验证并模拟真实的浏览器 | false |
| `css_selector` | string | 特定的 CSS 选择器，仅提取页面中的目标元素 | None |
| `js_code` | string | 提取之前在页面上执行的自定义 JavaScript 代码 | None |
| `session_id` | string | 持久化会话标识符，用于在多个请求间保留 Cookie 和浏览器状态 | None |
| `delay_before_return_html` | number | 提取 HTML 前等待的延迟时间（秒）（适用于重度 JS 的页面） | None |

## 👨‍💻 开发

如果您想修改爬虫或在本地运行：

1. 克隆此仓库：
```bash
git clone https://github.com/laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. 使用 `uv` 安装依赖：
```bash
uv sync
```

3. 使用官方的 MCP Inspector 在本地测试 MCP 服务器：
```bash
npx -y @modelcontextprotocol/inspector uv run crawl4ai-mcp
```

4. 运行自动化测试套件：
```bash
uv run pytest tests/
```

5. 直接运行 MCP 服务器（用于标准用途）：
```bash
uv run crawl4ai-mcp
```

## 🤝 贡献

欢迎贡献！请随时开启 issue 或提交 pull request。

## 📄 许可证

该项目根据 MIT 许可证授权 - 详情请参阅 LICENSE 文件。
