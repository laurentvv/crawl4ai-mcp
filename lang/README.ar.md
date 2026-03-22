# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

أداة قوية لزحف الويب تتكامل مع مساعدي الذكاء الاصطناعي عبر بروتوكول MCP (بروتوكول محادثة الآلة). يتيح لك هذا المشروع زحف مواقع الويب وحفظ محتواها [...]

## 📋 الميزات

- زحف مواقع الويب مع عمق قابل للتكوين
- دعم للروابط الداخلية والخارجية
- إنشاء ملفات ماركداون منظمة
- تكامل أصلي مع مساعدي الذكاء الاصطناعي عبر MCP
- إحصائيات مفصلة لنتائج الزحف
- معالجة الأخطاء والصفحات غير الموجودة

## 🚀 التثبيت

### المتطلبات الأساسية

- بايثون 3.9 أو أعلى

### خطوات التثبيت

1. استنساخ هذا المستودع:

```bash
git clone laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. إنشاء وتفعيل بيئة افتراضية:

```bash
# Windows
uv venv
source .venv/bin/activate

# Linux/MacOS
uv venv
source .venv/bin/activate
```

3. تثبيت التبعيات المطلوبة:

```bash
uv sync
```

## 🔧 التكوين

### تكوين MCP لمساعدي الذكاء الاصطناعي

لاستخدام هذا الزاحف مع مساعدي الذكاء الاصطناعي مثل VScode Cline، قم بتكوين ملف `cline_mcp_settings.json` الخاص بك:

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

استبدل `PATH\\TO\\YOUR\\ENVIRONMENT` و `PATH\\TO\\YOUR\\PROJECT` بالمسارات المناسبة على نظامك.

#### مثال ملموس (Windows)

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

## 🖥️ الاستخدام

### الاستخدام مع مساعد الذكاء الاصطناعي (عبر MCP)

بمجرد التكوين في مساعد الذكاء الاصطناعي الخاص بك، يمكنك استخدام الزاحف عن طريق مطالبة المساعد بإجراء عملية زحف باستخدام الصيغة التالية:

```
هل يمكنك زحف موقع الويب https://example.com بعمق 2؟
```

سيستخدم المساعد بروتوكول MCP لتشغيل أداة الزحف بالمعلمات المحددة.

### أمثلة الاستخدام مع Claude

فيما يلي أمثلة على الطلبات التي يمكنك تقديمها إلى Claude بعد تكوين أداة MCP:

- **زحف بسيط**: "هل يمكنك زحف موقع example.com وإعطائي ملخصًا؟"
- **زحف مع خيارات**: "هل يمكنك زحف https://example.com بعمق 3 وتضمين الروابط الخارجية؟"
- **زحف مع مخرجات مخصصة**: "هل يمكنك زحف مدونة example.com وحفظ النتائج في ملف يسمى 'blog_analysis.md'؟"

## 📁 هيكل النتائج

يتم حفظ نتائج الزحف في مجلد `crawl_results` في جذر المشروع. كل ملف نتيجة بتنسيق ماركداون مع الهيكل التالي:

```markdown
# https://example.com/page

## البيانات الوصفية
- العمق: 1
- الطابع الزمني: 2023-07-01T12:34:56

## المحتوى
المحتوى المستخرج من الصفحة...

---
```

## 🛠️ المعلمات المتاحة

تقبل أداة الزحف المعلمات التالية:

| المعلمة | النوع | الوصف | القيمة الافتراضية |
|-----------|------|-------------|---------------|
| url | سلسلة | عنوان URL للزحف (مطلوب) | - |
| max_depth | عدد صحيح | الحد الأقصى لعمق الزحف | 2 |
| include_external | منطقي | تضمين الروابط الخارجية | false |
| verbose | منطقي | تمكين المخرجات المفصلة | true |
| output_file | سلسلة | مسار ملف المخرجات | يتم إنشاؤه تلقائيًا |

## 📊 تنسيق النتائج

تعيد الأداة ملخصًا يحتوي على:
- عنوان URL الذي تم زحفه
- المسار إلى الملف الناتج
- مدة الزحف
- إحصائيات حول الصفحات المعالجة (ناجحة، فاشلة، غير موجودة، ممنوع الوصول)

يتم حفظ النتائج في دليل `crawl_results` لمشروعك.

## 🤝 المساهمة

المساهمات مرحب بها! لا تتردد في فتح قضية أو تقديم طلب سحب.

## 📄 الترخيص

هذا المشروع مرخص بموجب ترخيص MIT - راجع ملف LICENSE للتفاصيل.