# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

أداة قوية للزحف على الويب تتكامل مع مساعدي الذكاء الاصطناعي عبر بروتوكول سياق النموذج (MCP). يتيح هذا المشروع لمساعدي الذكاء الاصطناعي الزحف إلى المواقع الإلكترونية، واستخراج المحتوى الديناميكي، والتنقل عبر الروابط، وحفظ ملفات Markdown المنظمة مباشرة.

## 📋 المميزات

- تكامل أصلي مع مساعدي الذكاء الاصطناعي عبر MCP
- إرجاع محتوى Markdown المستخرج مباشرة إلى الذكاء الاصطناعي
- استخراج وعرض الروابط الداخلية/الخارجية للتنقل عبر الذكاء الاصطناعي
- انتظار محددات CSS الديناميكية قبل الاستخراج (دعم SPA)
- الزحف على المواقع الإلكترونية بعمق قابل للتهيئة
- إحصائيات مفصلة لنتائج الزحف
- معالجة الأخطاء وصفحات "غير موجود"

## 🚀 تهيئة MCP

الطريقة الأبسط والموصى بها لاستخدام هذه الأداة هي عبر `uvx` ، والتي تقوم تلقائيًا بجلب وتشغيل أحدث إصدار من GitHub دون مطالبتك باستنساخ المستودع يدويًا.

### المتطلبات الأساسية

- تثبيت [uv](https://github.com/astral-sh/uv) على نظامك.

### الإعداد لمساعدي الذكاء الاصطناعي (مثل Claude Desktop و Cline)

أضف ما يلي إلى ملف تهيئة MCP الخاص بمساعد الذكاء الاصطناعي (مثل `cline_mcp_settings.json` أو `claude_desktop_config.json`):

> **ملاحظة لمستخدمي ويندوز**: يوصى بشدة بتحديد `--python 3.12` لتجنب مشكلات الترجمة مع بعض التبعيات.

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

### هام: تثبيت المتصفح

يستخدم الزاحف Playwright للتعامل مع المحتوى الديناميكي. يجب عليك تثبيت المتصفحات المطلوبة بعد إعداد الأداة:

```bash
uv run playwright install chromium
```

## 🖥️ الاستخدام

بمجرد التهيئة، يمكنك استخدام الزاحف من خلال مطالبة مساعد الذكاء الاصطناعي الخاص بك بإجراء عملية زحف.

### أمثلة على الاستخدام مع Claude/Cline

- **زحف بسيط**: "هل يمكنك الزحف إلى موقع example.com وإعطائي ملخصًا؟"
- **زحف مع خيارات**: "هل يمكنك الزحف إلى https://example.com بعمق 3 وتضمين الروابط الخارجية؟"
- **المحتوى الديناميكي**: "قم بالزحف إلى تطبيق React هذا وانتظر تحميل محدد `.main-content`."

## 🛠️ المعلمات المتاحة (أداة MCP)

تقبل أداة `crawl` المعلمات التالية:

| المعلمة | النوع | الوصف | القيمة الافتراضية |
|-----------|------|-------------|---------------|
| `url` | string | رابط URL للزحف إليه (مطلوب) | - |
| `max_depth` | integer | أقصى عمق للزحف | 2 |
| `include_external` | boolean | تضمين الروابط الخارجية | false |
| `verbose` | boolean | تمكين المخرجات التفصيلية | true |
| `wait_for_selector` | string | محدد CSS للانتظار قبل استخراج المحتوى. مفيد لتطبيقات الصفحة الواحدة (SPA). | None |
| `return_content` | boolean | ما إذا كان سيتم إرجاع المحتوى المستخرج مباشرة في استجابة MCP (مقتطع إلى 50 ألف حرف إذا لزم الأمر). | true |
| `output_file` | string | مسار ملف المخرجات | يتم إنشاؤه تلقائيًا |

## 👨‍💻 التطوير

إذا كنت ترغب في تعديل الزاحف أو تشغيله محليًا:

1. استنساخ هذا المستودع:
```bash
git clone https://github.com/laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. تثبيت التبعيات باستخدام `uv`:
```bash
uv sync
```

3. تشغيل خادم MCP مباشرة:
```bash
uv run crawl4ai-mcp
```

## 🤝 المساهمة

المساهمات مرحب بها! لا تتردد في فتح مشكلة (issue) أو تقديم طلب سحب (pull request).

## 📄 الترخيص

هذا المشروع مرخص بموجب رخصة MIT - راجع ملف LICENSE للحصول على التفاصيل.
