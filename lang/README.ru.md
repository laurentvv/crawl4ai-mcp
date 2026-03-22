# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Мощный инструмент для веб-краулинга, который интегрируется с ИИ-ассистентами через MCP (Machine Conversation Protocol). Этот проект позволяет вам сканировать веб-сайты и сохранять их содержимое [...]

## 📋 Функции

- Сканирование веб-сайтов с настраиваемой глубиной
- Поддержка внутренних и внешних ссылок
- Создание структурированных Markdown файлов
- Нативная интеграция с ИИ-ассистентами через MCP
- Подробная статистика результатов сканирования
- Обработка ошибок и ненайденных страниц

## 🚀 Установка

### Предварительные требования

- Python 3.9 или выше

### Шаги установки

1. Клонируйте этот репозиторий:

```bash
git clone laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Создайте и активируйте виртуальную среду:

```bash
# Windows
uv venv
source .venv/bin/activate

# Linux/MacOS
uv venv
source .venv/bin/activate
```

3. Установите необходимые зависимости:

```bash
uv sync
```

## 🔧 Конфигурация

### Конфигурация MCP для ИИ-ассистентов

Для использования этого краулера с ИИ-ассистентами, такими как VScode Cline, настройте ваш файл `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "crawl": {
      "command": "uv",
      "args": [
        "run",
        "PATH\\TO\\YOUR\\PROJECT\\crawl_mcp.py"
      ],
      "disabled": false,
      "autoApprove": [],
      "timeout": 600
    }
  }
}
```

Замените `PATH\\TO\\YOUR\\ENVIRONMENT` и `PATH\\TO\\YOUR\\PROJECT` соответствующими путями в вашей системе.

#### Конкретный пример (Windows)

```json
{
  "mcpServers": {
    "crawl": {
      "command": "uv",
      "args": [
        "run",
        "D:\\Python\\crawl4ai-mcp\\crawl_mcp.py"
      ],
      "disabled": false,
      "autoApprove": [],
      "timeout": 600
    }
  }
}
```

## 🖥️ Использование

### Использование с ИИ-ассистентом (через MCP)

После настройки в вашем ИИ-ассистенте вы можете использовать краулер, попросив ассистента выполнить сканирование с использованием следующего синтаксиса:

```
Можете вы сканировать веб-сайт https://example.com с глубиной 2?
```

Ассистент будет использовать протокол MCP для запуска инструмента сканирования с указанными параметрами.

### Примеры использования с Claude

Вот примеры запросов, которые вы можете сделать Claude после настройки инструмента MCP:

- **Простое сканирование**: "Можете вы сканировать сайт example.com и дать мне резюме?"
- **Сканирование с опциями**: "Можете вы сканировать https://example.com с глубиной 3 и включить внешние ссылки?"
- **Сканирование с пользовательским выводом**: "Можете вы сканировать блог example.com и сохранить результаты в файл с именем 'blog_analysis.md'?"

## 📁 Структура результатов

Результаты сканирования сохраняются в папке `crawl_results` в корне проекта. Каждый файл результатов в формате Markdown имеет следующую структуру:

```markdown
# https://example.com/page

## Метаданные
- Глубина: 1
- Временная метка: 2023-07-01T12:34:56

## Содержание
Извлеченное содержимое страницы...

---
```

## 🛠️ Доступные параметры

Инструмент сканирования принимает следующие параметры:

| Параметр | Тип | Описание | Значение по умолчанию |
|-----------|------|-------------|---------------|
| url | строка | URL для сканирования (обязательно) | - |
| max_depth | целое число | Максимальная глубина сканирования | 2 |
| include_external | логический | Включать внешние ссылки | false |
| verbose | логический | Включить подробный вывод | true |
| output_file | строка | Путь выходного файла | автоматически генерируется |

## 📊 Формат результата

Инструмент возвращает резюме с:
- Просканированный URL
- Путь к сгенерированному файлу
- Продолжительность сканирования
- Статистика обработанных страниц (успешных, неудачных, не найденных, доступ запрещен)

Результаты сохраняются в директории `crawl_results` вашего проекта.

## 🤝 Вклад

Вклады приветствуются! Не стесняйтесь открыть issue или отправить pull request.

## 📄 Лицензия

Этот проект лицензирован под MIT License - смотрите файл LICENSE для деталей.