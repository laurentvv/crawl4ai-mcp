# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Una potente herramienta de rastreo web que se integra con asistentes de IA a través del MCP (Protocolo de Conversación de Máquina). Este proyecto te permite rastrear sitios web y guardar su contenido [...]

## 📋 Características

- Rastreo de sitios web con profundidad configurable
- Soporte para enlaces internos y externos
- Generación de archivos Markdown estructurados
- Integración nativa con asistentes de IA a través de MCP
- Estadísticas detalladas de resultados de rastreo
- Manejo de errores y páginas no encontradas

## 🚀 Instalación

### Requisitos previos

- Python 3.9 o superior

### Pasos de instalación

1. Clona este repositorio:

```bash
git clone laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Crea y activa un entorno virtual:

```bash
# Windows
uv venv
source .venv/bin/activate

# Linux/MacOS
uv venv
source .venv/bin/activate
```

3. Instala las dependencias requeridas:

```bash
uv sync
```

## 🔧 Configuración

### Configuración MCP para Asistentes de IA

Para usar este rastreador con asistentes de IA como VScode Cline, configura tu archivo `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "crawl": {
      "command": "uvx",
      "args": [
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

Reemplaza `PATH\\TO\\YOUR\\ENVIRONMENT` y `PATH\\TO\\YOUR\\PROJECT` con las rutas apropiadas en tu sistema.

#### Ejemplo concreto (Windows)

```json
{
  "mcpServers": {
    "crawl": {
      "command": "uvx",
      "args": [
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

## 🖥️ Uso

### Uso con un Asistente de IA (a través de MCP)

Una vez configurado en tu asistente de IA, puedes usar el rastreador pidiéndole al asistente que realice un rastreo utilizando la siguiente sintaxis:

```
¿Puedes rastrear el sitio web https://example.com con una profundidad de 2?
```

El asistente utilizará el protocolo MCP para ejecutar la herramienta de rastreo con los parámetros especificados.

### Ejemplos de uso con Claude

Aquí hay ejemplos de solicitudes que puedes hacer a Claude después de configurar la herramienta MCP:

- **Rastreo simple**: "¿Puedes rastrear el sitio example.com y darme un resumen?"
- **Rastreo con opciones**: "¿Puedes rastrear https://example.com con una profundidad de 3 e incluir enlaces externos?"
- **Rastreo con salida personalizada**: "¿Puedes rastrear el blog example.com y guardar los resultados en un archivo llamado 'blog_analysis.md'?"

## 📁 Estructura de resultados

Los resultados del rastreo se guardan en la carpeta `crawl_results` en la raíz del proyecto. Cada archivo de resultados está en formato Markdown con la siguiente estructura:

```markdown
# https://example.com/page

## Metadatos
- Profundidad: 1
- Marca de tiempo: 2023-07-01T12:34:56

## Contenido
Contenido extraído de la página...

---
```

## 🛠️ Parámetros disponibles

La herramienta de rastreo acepta los siguientes parámetros:

| Parámetro | Tipo | Descripción | Valor predeterminado |
|-----------|------|-------------|---------------|
| url | string | URL a rastrear (requerido) | - |
| max_depth | integer | Profundidad máxima de rastreo | 2 |
| include_external | boolean | Incluir enlaces externos | false |
| verbose | boolean | Habilitar salida detallada | true |
| wait_for_selector | string | CSS selector to wait for before extracting content. | None |
| return_content | boolean | Whether to return the extracted content directly in the MCP response | true |
| output_file | string | Ruta del archivo de salida | generada automáticamente |

## 📊 Formato de resultado

La herramienta devuelve un resumen con:
- URL rastreada
- Ruta al archivo generado
- Duración del rastreo
- Estadísticas sobre las páginas procesadas (exitosas, fallidas, no encontradas, acceso prohibido)

Los resultados se guardan en el directorio `crawl_results` de tu proyecto.

## 🤝 Contribución

¡Las contribuciones son bienvenidas! No dudes en abrir un issue o enviar un pull request.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.