# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Uma poderosa ferramenta de rastreamento web que se integra com assistentes de IA através do MCP (Machine Conversation Protocol). Este projeto permite que você rastreie sites e salve seu conteúdo [...]

## 📋 Recursos

- Rastreamento de sites com profundidade configurável
- Suporte para links internos e externos
- Geração de arquivos Markdown estruturados
- Integração nativa com assistentes de IA via MCP
- Estatísticas detalhadas dos resultados de rastreamento
- Tratamento de erros e páginas não encontradas

## 🚀 Instalação

### Pré-requisitos

- Python 3.9 ou superior

### Passos de instalação

1. Clone este repositório:

```bash
git clone laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Crie e ative um ambiente virtual:

```bash
# Windows
uv venv
source .venv/bin/activate

# Linux/MacOS
uv venv
source .venv/bin/activate
```

3. Instale as dependências necessárias:

```bash
uv sync
```

## 🔧 Configuração

### Configuração MCP para Assistentes de IA

Para usar este rastreador com assistentes de IA como VScode Cline, configure seu arquivo `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "crawl": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/laurentvv/crawl4ai-mcp",
        "crawl4ai-mcp"
        "PATH\\TO\\YOUR\\PROJECT\\crawl_mcp.py"
      ],
      "disabled": false,
      "autoApprove": [],
      "timeout": 600
    }
  }
}
```

Substitua `PATH\\TO\\YOUR\\ENVIRONMENT` e `PATH\\TO\\YOUR\\PROJECT` pelos caminhos apropriados no seu sistema.

#### Exemplo Concreto (Windows)

```json
{
  "mcpServers": {
    "crawl": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/laurentvv/crawl4ai-mcp",
        "crawl4ai-mcp"
        "D:\\Python\\crawl4ai-mcp\\crawl_mcp.py"
      ],
      "disabled": false,
      "autoApprove": [],
      "timeout": 600
    }
  }
}
```

## 🖥️ Uso

### Uso com um Assistente de IA (via MCP)

Uma vez configurado em seu assistente de IA, você pode usar o rastreador pedindo ao assistente para realizar um rastreamento usando a seguinte sintaxe:

```
Você pode rastrear o site https://example.com com uma profundidade de 2?
```

O assistente usará o protocolo MCP para executar a ferramenta de rastreamento com os parâmetros especificados.

### Exemplos de uso com Claude

Aqui estão exemplos de solicitações que você pode fazer ao Claude após configurar a ferramenta MCP:

- **Rastreamento simples**: "Você pode rastrear o site example.com e me dar um resumo?"
- **Rastreamento com opções**: "Você pode rastrear https://example.com com uma profundidade de 3 e incluir links externos?"
- **Rastreamento com saída personalizada**: "Você pode rastrear o blog example.com e salvar os resultados em um arquivo chamado 'blog_analysis.md'?"

## 📁 Estrutura de Resultados

Os resultados do rastreamento são salvos na pasta `crawl_results` na raiz do projeto. Cada arquivo de resultado está em formato Markdown com a seguinte estrutura:

```markdown
# https://example.com/page

## Metadados
- Profundidade: 1
- Timestamp: 2023-07-01T12:34:56

## Conteúdo
Conteúdo extraído da página...

---
```

## 🛠️ Parâmetros Disponíveis

A ferramenta de rastreamento aceita os seguintes parâmetros:

| Parâmetro | Tipo | Descrição | Valor Padrão |
|-----------|------|-------------|---------------|
| url | string | URL para rastrear (obrigatório) | - |
| max_depth | inteiro | Profundidade máxima de rastreamento | 2 |
| include_external | booleano | Incluir links externos | false |
| verbose | booleano | Ativar saída detalhada | true |
| output_file | string | Caminho do arquivo de saída | gerado automaticamente |

## 📊 Formato do Resultado

A ferramenta retorna um resumo com:
- URL rastreada
- Caminho para o arquivo gerado
- Duração do rastreamento
- Estatísticas sobre páginas processadas (bem-sucedidas, falhas, não encontradas, acesso proibido)

Os resultados são salvos no diretório `crawl_results` do seu projeto.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.