# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Мощный инструмент для веб-краулинга, который интегрируется с ИИ-ассистентами через MCP (Model Context Protocol). Этот проект позволяет ИИ-ассистентам сканировать веб-сайты, извлекать динамический контент, переходить по ссылкам и напрямую сохранять структурированные файлы Markdown.

## 📋 Возможности

- Нативная интеграция с ИИ-ассистентами через MCP
- Прямой возврат извлеченного Markdown-контента ИИ
- Извлечение и отображение внутренних/внешних ссылок для навигации ИИ
- Ожидание динамических CSS-селекторов перед извлечением (поддержка SPA)
- Веб-краулинг с настраиваемой глубиной
- Детальная статистика результатов сканирования
- Обработка ошибок и страниц «не найдено»

## 🚀 Настройка MCP

Самый простой и рекомендуемый способ использования этого инструмента — через `uvx`, который автоматически загружает и запускает последнюю версию с GitHub без необходимости ручного клонирования репозитория.

### Предварительные требования

- Установленный [uv](https://github.com/astral-sh/uv) в вашей системе.

### Настройка для ИИ-ассистентов (например, Claude Desktop, Cline)

Добавьте следующее в файл конфигурации MCP вашего ИИ-ассистента (например, `cline_mcp_settings.json` или `claude_desktop_config.json`):

> **Примечание для пользователей Windows**: Настоятельно рекомендуется указать `--python 3.12`, чтобы избежать проблем с компиляцией некоторых зависимостей.

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

### Важно: Установка браузера

Краулер использует Playwright для работы с динамическим контентом. Вы должны установить необходимые браузеры после настройки инструмента:

```bash
uv run playwright install chromium
```

## 🖥️ Использование

После настройки вы можете использовать краулер, попросив своего ИИ-ассистента выполнить сканирование.

### Примеры использования с Claude/Cline

- **Простое сканирование**: «Можешь просканировать сайт example.com и дать мне краткое описание?»
- **Сканирование с опциями**: «Просканируй https://example.com с глубиной 3 и включи внешние ссылки».
- **Динамический контент**: «Просканируй это React-приложение и дождись загрузки селектора `.main-content`».

## 🛠️ Доступные параметры (Инструмент MCP)

Инструмент `crawl` принимает следующие параметры:

| Параметр | Тип | Описание | Значение по умолчанию |
|----------|-----|----------|-----------------------|
| `url` | string | URL для сканирования (обязательно) | - |
| `max_depth` | integer | Максимальная глубина сканирования | 2 |
| `include_external` | boolean | Включать внешние ссылки | false |
| `verbose` | boolean | Включить подробный вывод | true |
| `wait_for_selector` | string | CSS-селектор для ожидания перед извлечением контента. Полезно для одностраничных приложений (SPA). | None |
| `return_content` | boolean | Возвращать ли извлеченный контент напрямую в ответе MCP (обрезается до 50 тыс. символов при необходимости). | true |
| `output_file` | string | Путь к выходному файлу | создается автоматически |

## 👨‍💻 Разработка

Если вы хотите изменить краулер или запустить его локально:

1. Клонируйте этот репозиторий:
```bash
git clone https://github.com/laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Установите зависимости с помощью `uv`:
```bash
uv sync
```

3. Запустите сервер MCP напрямую:
```bash
uv run crawl4ai-mcp
```

## 🤝 Участие в проекте

Будем рады вашему вкладу! Не стесняйтесь открывать issue или отправлять pull request.

## 📄 Лицензия

Этот проект лицензирован на условиях лицензии MIT — подробности см. в файле LICENSE.
