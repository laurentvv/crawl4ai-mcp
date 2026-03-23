# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Uma poderosa ferramenta de rastreamento web que se integra com assistentes de IA através do MCP (Model Context Protocol). Este projeto permite que assistentes de IA rastreiem sites, extraiam conteúdo dinâmico, naveguem através de links e salvem arquivos Markdown estruturados diretamente.

## 📋 Funcionalidades

- Integração nativa com assistentes de IA via MCP
- Retorna o conteúdo Markdown extraído diretamente para a IA
- Extrai e exibe links internos/externos para navegação da IA
- Aguarda seletores CSS dinâmicos antes da extração (suporte a SPA)
- Rastreamento de sites com profundidade configurável
- Estatísticas detalhadas dos resultados do rastreamento
- Tratamento de erros e páginas não encontradas

## 🚀 Configuração do MCP

A maneira mais simples e recomendada de usar esta ferramenta é via `uvx`, que baixa e executa automaticamente a versão mais recente do GitHub sem a necessidade de clonar o repositório manualmente.

### Pré-requisitos

- [uv](https://github.com/astral-sh/uv) instalado no seu sistema.

### Configuração para Assistentes de IA (ex: Claude Desktop, Cline)

Adicione o seguinte ao arquivo de configuração MCP do seu assistente de IA (ex: `cline_mcp_settings.json` ou `claude_desktop_config.json`):

> **Nota para usuários Windows**: É altamente recomendável especificar `--python 3.12` para evitar problemas de compilação com certas dependências.

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

### Importante: Instalação do Navegador

O rastreador usa Playwright para lidar com conteúdo dinâmico. Você deve instalar os navegadores necessários após configurar a ferramenta:

```bash
uv run playwright install chromium
```

## 🖥️ Uso

Uma vez configurado, você pode usar o rastreador pedindo ao seu assistente de IA para realizar um rastreamento.

### Exemplos de Uso com Claude/Cline

- **Rastreamento Simples**: "Você pode rastrear o site example.com e me dar um resumo?"
- **Rastreamento com Opções**: "Você pode rastrear https://example.com com uma profundidade de 3 e incluir links externos?"
- **Conteúdo Dinâmico**: "Rastreie este app React e aguarde o seletor `.main-content` carregar."

## 🛠️ Parámetros Disponíveis (Ferramenta MCP)

A ferramenta `crawl` aceita os seguintes parâmetros:

| Parâmetro | Tipo | Descrição | Valor Padrão |
|-----------|------|-------------|--------------|
| `url` | string | URL para rastrear (obrigatório) | - |
| `max_depth` | integer | Profundidade máxima de rastreamento | 2 |
| `include_external` | boolean | Incluir links externos | false |
| `verbose` | boolean | Habilitar saída detalhada | true |
| `wait_for_selector` | string | Seletor CSS a aguardar antes de extrair o conteúdo. Útil para aplicações de página única (SPA). | None |
| `return_content` | boolean | Se deve retornar o conteúdo extraído diretamente na resposta MCP (truncado para 50k caracteres se necessário). | true |
| `output_file` | string | Caminho do arquivo de saída | gerado automaticamente |

## 👨‍💻 Desenvolvimento

Se você deseja modificar o rastreador ou executá-lo localmente:

1. Clone este repositório:
```bash
git clone https://github.com/laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Instale as dependências usando `uv`:
```bash
uv sync
```

3. Execute o servidor MCP diretamente:
```bash
uv run crawl4ai-mcp
```

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.
