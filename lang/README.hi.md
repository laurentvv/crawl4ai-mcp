# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

एक शक्तिशाली वेब क्रॉलिंग टूल जो MCP (मशीन कन्वर्सेशन प्रोटोकॉल) के माध्यम से AI सहायकों के साथ एकीकृत होता है। यह प्रोजेक्ट आपको वेबसाइटों को क्रॉल करने और उनकी सामग्री को सहेजने की अनुमति देता है [...]

## 📋 विशेषताएँ

- कॉन्फ़िगर करने योग्य गहराई के साथ वेबसाइट क्रॉलिंग
- आंतरिक और बाहरी लिंक के लिए समर्थन
- संरचित मार्कडाउन फाइलों का निर्माण
- MCP के माध्यम से AI सहायकों के साथ मूल एकीकरण
- विस्तृत क्रॉल परिणाम आंकड़े
- त्रुटि और नहीं मिले पृष्ठ हैंडलिंग

## 🚀 इंस्टॉलेशन

### पूर्वापेक्षाएँ

- Python 3.9 या उच्चतर

### इंस्टॉलेशन के चरण

1. इस रिपॉजिटरी को क्लोन करें:

```bash
git clone laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. वर्चुअल एनवायरनमेंट बनाएं और सक्रिय करें:

```bash
# Windows
uv venv
source .venv/bin/activate

# Linux/MacOS
uv venv
source .venv/bin/activate
```

3. आवश्यक डिपेंडेंसीज इंस्टॉल करें:

```bash
uv sync
```

## 🔧 कॉन्फ़िगरेशन

### AI सहायकों के लिए MCP कॉन्फ़िगरेशन

इस क्रॉलर को VScode Cline जैसे AI सहायकों के साथ उपयोग करने के लिए, अपनी `cline_mcp_settings.json` फ़ाइल कॉन्फ़िगर करें:

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

`PATH\\TO\\YOUR\\ENVIRONMENT` और `PATH\\TO\\YOUR\\PROJECT` को अपने सिस्टम पर उपयुक्त पथों से बदलें।

#### ठोस उदाहरण (Windows)

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

## 🖥️ उपयोग

### AI सहायक के साथ उपयोग (MCP के माध्यम से)

अपने AI सहायक में कॉन्फ़िगर करने के बाद, आप निम्नलिखित सिंटैक्स का उपयोग करके सहायक से क्रॉल करने के लिए कह सकते हैं:

```
क्या आप वेबसाइट https://example.com को 2 की गहराई के साथ क्रॉल कर सकते हैं?
```

सहायक निर्दिष्ट पैरामीटर के साथ क्रॉलिंग टूल चलाने के लिए MCP प्रोटोकॉल का उपयोग करेगा।

### क्लाउड के साथ उपयोग के उदाहरण

MCP टूल कॉन्फ़िगर करने के बाद, आप क्लाउड को कर सकते हैं निम्न अनुरोध:

- **सरल क्रॉल**: "क्या आप example.com साइट को क्रॉल कर सकते हैं और मुझे सारांश दे सकते हैं?"
- **विकल्पों के साथ क्रॉल**: "क्या आप https://example.com को 3 की गहराई के साथ क्रॉल कर सकते हैं और बाहरी लिंक शामिल कर सकते हैं?"
- **कस्टम आउटपुट के साथ क्रॉल**: "क्या आप ब्लॉग example.com को क्रॉल कर सकते हैं और परिणामों को 'blog_analysis.md' नामक फ़ाइल में सहेज सकते हैं?"

## 📁 परिणाम संरचना

क्रॉल परिणाम प्रोजेक्ट के रूट में `crawl_results` फ़ोल्डर में सहेजे जाते हैं। प्रत्येक परिणाम फ़ाइल मार्कडाउन प्रारूप में निम्नलिखित संरचना के साथ होती है:

```markdown
# https://example.com/page

## मेटाडेटा
- गहराई: 1
- टाइमस्टैम्प: 2023-07-01T12:34:56

## सामग्री
पेज से निकाली गई सामग्री...

---
```

## 🛠️ उपलब्ध पैरामीटर्स

क्रॉल टूल निम्नलिखित पैरामीटर स्वीकार करता है:

| पैरामीटर | प्रकार | विवरण | डिफ़ॉल्ट मान |
|-----------|------|-------------|---------------|
| url | स्ट्रिंग | क्रॉल करने के लिए URL (आवश्यक) | - |
| max_depth | इंटीजर | अधिकतम क्रॉलिंग गहराई | 2 |
| include_external | बूलियन | बाहरी लिंक शामिल करें | false |
| verbose | बूलियन | विस्तृत आउटपुट सक्षम करें | true |
| wait_for_selector | string | CSS selector to wait for before extracting content. | None |
| return_content | boolean | Whether to return the extracted content directly in the MCP response | true |
| output_file | स्ट्रिंग | आउटपुट फ़ाइल पथ | स्वचालित रूप से उत्पन्न |

## 📊 परिणाम प्रारूप

टूल निम्नलिखित के साथ एक सारांश लौटाता है:
- क्रॉल किया गया URL
- उत्पन्न फ़ाइल का पथ
- क्रॉल की अवधि
- प्रोसेस किए गए पेजों के आंकड़े (सफल, असफल, नहीं मिला, एक्सेस निषेध)

परिणाम आपके प्रोजेक्ट की `crawl_results` डायरेक्टरी में सहेजे जाते हैं।

## 🤝 योगदान

योगदान स्वागत योग्य हैं! बेझिझक एक मुद्दा खोलें या पुल अनुरोध सबमिट करें।

## 📄 लाइसेंस

यह प्रोजेक्ट MIT लाइसेंस के तहत लाइसेंस प्राप्त है - विवरण के लिए LICENSE फ़ाइल देखें।