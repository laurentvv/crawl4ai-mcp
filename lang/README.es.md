# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Una potente herramienta de rastreo web que se integra con asistentes de IA a través del MCP (Model Context Protocol). Este proyecto permite a los asistentes de IA rastrear sitios web, extraer contenido dinámico, navegar a través de enlaces y guardar archivos Markdown estructurados directamente.

## 📋 Características

- Integración nativa con asistentes de IA a través de MCP
- Devuelve el contenido Markdown extraído directamente a la IA
- Extrae y muestra enlaces internos/externos para la navegación de la IA
- Espera a selectores CSS dinámicos antes de extraer (soporte para SPA)
- Rastreo de sitios web con profundidad configurable
- Estadísticas detalladas de los resultados del rastreo
- Manejo de errores y páginas no encontradas

## 🚀 Configuración de MCP

La forma más sencilla y recomendada de usar esta herramienta es a través de `uvx`, que descarga y ejecuta automáticamente la última versión desde GitHub sin necesidad de clonar el repositorio manualmente.

### Requisitos previos

- [uv](https://github.com/astral-sh/uv) instalado en su sistema.

### Configuración para asistentes de IA (por ejemplo, Claude Desktop, Cline)

Agregue lo siguiente al archivo de configuración de MCP de su asistente de IA (por ejemplo, `cline_mcp_settings.json` o `claude_desktop_config.json`):

> **Nota para usuarios de Windows**: Se recomienda encarecidamente especificar `--python 3.12` para evitar problemas de compilación con ciertas dependencias.

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

### Importante: Instalación del navegador

El rastreador utiliza Playwright para manejar contenido dinámico. Debe instalar los navegadores necesarios después de configurar la herramienta:

```bash
uv run playwright install chromium
```

## 🖥️ Uso

Una vez configurado, puede usar el rastreador pidiendo a su asistente de IA que realice un rastreo.

### Ejemplos de uso con Claude/Cline

- **Rastreo simple**: "¿Puedes rastrear el sitio example.com y darme un resumen?"
- **Rastreo con opciones**: "¿Puedes rastrear https://example.com con una profundidad de 3 e incluir enlaces externos?"
- **Contenido dinámico**: "Rastrea esta aplicación React y espera a que se cargue el selector `.main-content`."

## 🛠️ Parámetros disponibles (Herramienta MCP)

La herramienta `crawl` acepta los siguientes parámetros:

| Parámetro | Tipo | Descripción | Valor predeterminado |
|-----------|------|-------------|---------------|
| `url` | string | URL a rastrear (requerido) | - |
| `max_depth` | integer | Profundidad máxima de rastreo | 2 |
| `include_external` | boolean | Incluir enlaces externos | false |
| `verbose` | boolean | Habilitar salida detallada | true |
| `wait_for_selector` | string | Selector CSS a esperar antes de extraer el contenido. Útil para aplicaciones de una sola página (SPA). | None |
| `return_content` | boolean | Si se debe devolver el contenido extraído directamente en la respuesta MCP (truncado a 50k caracteres si es necesario). | true |
| `output_file` | string | Ruta del archivo de salida | generado automáticamente |

## 👨‍💻 Desarrollo

Si desea modificar el rastreador o ejecutarlo localmente:

1. Clone este repositorio:
```bash
git clone https://github.com/laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Instale las dependencias usando `uv`:
```bash
uv sync
```

3. Ejecute el servidor MCP directamente:
```bash
uv run crawl4ai-mcp
```

## 🤝 Contribución

¡Las contribuciones son bienvenidas! No dude en abrir un issue o enviar un pull request.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulte el archivo LICENSE para más detalles.
