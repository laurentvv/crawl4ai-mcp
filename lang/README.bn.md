# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

একটি শক্তিশালী ওয়েব ক্রলিং টুল যা MCP (মেশিন কনভার্সেশন প্রোটোকল) এর মাধ্যমে AI সহায়কদের সাথে সংযুক্ত হয়। এই প্রকল্পটি আপনাকে ওয়েবসাইট ক্রল করতে এবং তাদের বিষয়বস্তু সংরক্ষণ করতে দেয় [...]

## 📋 বৈশিষ্ট্য

- কনফিগারযোগ্য গভীরতা সহ ওয়েবসাইট ক্রলিং
- অভ্যন্তরীণ এবং বাহ্যিক লিঙ্কের সমর্থন
- কাঠামোগত মার্কডাউন ফাইল তৈরি
- MCP এর মাধ্যমে AI সহায়কদের সাথে নেটিভ ইন্টিগ্রেশন
- বিস্তারিত ক্রল ফলাফলের পরিসংখ্যান
- ত্রুটি এবং পাওয়া যায়নি পৃষ্ঠা হ্যান্ডলিং

## 🚀 ইনস্টলেশন

### পূর্বশর্ত

- পাইথন 3.9 বা উচ্চতর

### ইনস্টলেশন ধাপ

1. এই রিপোজিটরি ক্লোন করুন:

```bash
git clone laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. একটি ভার্চুয়াল এনভায়রনমেন্ট তৈরি এবং সক্রিয় করুন:

```bash
# Windows
uv venv
source .venv/bin/activate

# Linux/MacOS
uv venv
source .venv/bin/activate
```

3. প্রয়োজনীয় নির্ভরতাগুলি ইনস্টল করুন:

```bash
uv sync
```

## 🔧 কনফিগারেশন

### AI সহায়কদের জন্য MCP কনফিগারেশন

VScode Cline এর মতো AI সহায়কদের সাথে এই ক্রলার ব্যবহার করতে, আপনার `cline_mcp_settings.json` ফাইল কনফিগার করুন:

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

`PATH\\TO\\YOUR\\ENVIRONMENT` এবং `PATH\\TO\\YOUR\\PROJECT` কে আপনার সিস্টেমের উপযুক্ত পাথ দিয়ে প্রতিস্থাপন করুন।

#### বাস্তব উদাহরণ (Windows)

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

## 🖥️ ব্যবহার

### AI সহায়কের সাথে ব্যবহার (MCP এর মাধ্যমে)

আপনার AI সহায়কের মধ্যে কনফিগার করার পরে, আপনি নিম্নলিখিত সিনট্যাক্স ব্যবহার করে সহায়ককে ক্রল করতে বলে ক্রলার ব্যবহার করতে পারেন:

```
আপনি কি https://example.com ওয়েবসাইটটি 2 গভীরতা সহ ক্রল করতে পারেন?
```

সহায়ক নির্দিষ্ট প্যারামিটারগুলি সহ ক্রলিং টুল চালানোর জন্য MCP প্রোটোকল ব্যবহার করবে।

### Claude এর সাথে ব্যবহারের উদাহরণ

MCP টুল কনফিগার করার পরে আপনি Claude কে যে অনুরোধগুলি করতে পারেন তার উদাহরণ এখানে দেওয়া হল:

- **সাধারণ ক্রল**: "আপনি কি example.com সাইটটি ক্রল করে আমাকে একটি সারাংশ দিতে পারেন?"
- **অপশন সহ ক্রল**: "আপনি কি https://example.com কে 3 গভীরতা সহ ক্রল করতে পারেন এবং বাহ্যিক লিঙ্কগুলি অন্তর্ভুক্ত করতে পারেন?"
- **কাস্টম আউটপুট সহ ক্রল**: "আপনি কি example.com ব্লগ ক্রল করতে পারেন এবং ফলাফলগুলি 'blog_analysis.md' নামে একটি ফাইলে সংরক্ষণ করতে পারেন?"

## 📁 ফলাফল কাঠামো

ক্রল ফলাফলগুলি প্রকল্পের রুটের `crawl_results` ফোল্ডারে সংরক্ষিত হয়। প্রতিটি ফলাফল ফাইল নিম্নলিখিত কাঠামো সহ মার্কডাউন ফরম্যাটে থাকে:

```markdown
# https://example.com/page

## মেটাডাটা
- গভীরতা: 1
- টাইমস্ট্যাম্প: 2023-07-01T12:34:56

## বিষয়বস্তু
পৃষ্ঠা থেকে নিষ্কাশিত বিষয়বস্তু...

---
```

## 🛠️ উপলব্ধ প্যারামিটার

ক্রল টুল নিম্নলিখিত প্যারামিটারগুলি গ্রহণ করে:

| প্যারামিটার | টাইপ | বর্ণনা | ডিফল্ট মান |
|-----------|------|-------------|---------------|
| url | স্ট্রিং | ক্রল করার URL (প্রয়োজনীয়) | - |
| max_depth | ইন্টিজার | সর্বাধিক ক্রলিং গভীরতা | 2 |
| include_external | বুলিয়ান | বাহ্যিক লিঙ্ক অন্তর্ভুক্ত করুন | false |
| verbose | বুলিয়ান | বিস্তারিত আউটপুট সক্ষম করুন | true |
| output_file | স্ট্রিং | আউটপুট ফাইল পাথ | স্বয়ংক্রিয়ভাবে তৈরি |

## 📊 ফলাফল ফরম্যাট

টুলটি নিম্নলিখিত বিষয়গুলি সহ একটি সারাংশ প্রদান করে:
- ক্রল করা URL
- তৈরি ফাইলের পাথ
- ক্রলের সময়কাল
- প্রক্রিয়াকৃত পৃষ্ঠা সম্পর্কে পরিসংখ্যান (সফল, ব্যর্থ, পাওয়া যায়নি, অ্যাক্সেস নিষিদ্ধ)

ফলাফলগুলি আপনার প্রকল্পের `crawl_results` ডিরেক্টরিতে সংরক্ষিত হয়।

## 🤝 অবদান

অবদান স্বাগত! একটি ইস্যু খোলতে বা একটি পুল রিকোয়েস্ট জমা দিতে দ্বিধা করবেন না।

## 📄 লাইসেন্স

এই প্রকল্পটি MIT লাইসেন্সের অধীনে লাইসেন্সকৃত - বিস্তারিত জানার জন্য LICENSE ফাইল দেখুন।