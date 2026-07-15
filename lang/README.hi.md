# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

<div align="center">
  <img src="../assets/banner.jpg" alt="Crawl4AI MCP Banner" width="800"/>
</div>

एक शक्तिशाली वेब क्रॉलिंग टूल जो MCP (Model Context Protocol) के माध्यम से AI सहायकों के साथ एकीकृत होता है। यह प्रोजेक्ट AI सहायकों को वेबसाइटों को क्रॉल करने, डायनेमिक कंटेंट निकालने, लिंक के माध्यम से नेविगेट करने और सीधे संरचित मार्कडाउन फ़ाइलों को सहेजने की अनुमति देता है।

## 📋 विशेषताएं

- MCP के माध्यम से AI सहायकों के साथ नेटिव एकीकरण
- स्क्रैप किए गए मार्कडाउन कंटेंट को सीधे AI को वापस भेजना
- AI नेविगेशन के लिए आंतरिक/बाहरी लिंक निकालना और प्रदर्शित करना
- कॉन्फ़िगर करने योग्य गहराई के साथ वेबसाइट क्रॉलिंग
- विस्तृत क्रॉल परिणाम आंकड़े
- त्रुटि और 'पेज नहीं मिला' (not found) हैंडलिंग
- **उन्नत स्क्रैपिंग क्षमताएं (Advanced Scraping Capabilities)**:
  - **मैजिक मोड (Magic Mode)**: एंटी-बॉट्स (जैसे Cloudflare) को बायपास करें और वास्तविक ब्राउज़र व्यवहार का अनुकरण करें
  - **लक्षित निष्कर्षण (Targeted Extraction)**: CSS सिलेक्टर्स का उपयोग करके केवल वही प्राप्त करें जो आपको चाहिए
  - **कस्टम जावास्क्रिप्ट (Custom JavaScript)**: निष्कर्षण से पहले कोड निष्पादित करें (क्लिक, स्क्रॉल, फॉर्म भरना)
  - **स्थायी सत्र (Persistent Sessions)**: प्रमाणित साइटों के लिए अनुरोधों के बीच कुकीज़ और स्थिति बनाए रखें
  - **SPA समर्थन (SPA Support)**: डायनेमिक CSS सिलेक्टर्स की प्रतीक्षा करें या स्पष्ट प्री-एक्सट्रैक्शन देरी सेट करें

## 🚀 MCP कॉन्फ़िगरेशन

इस टूल का उपयोग करने का सबसे सरल और अनुशंसित तरीका `uvx` के माध्यम से है, जो मैन्युअल रूप से रिपॉजिटरी को क्लोन किए बिना स्वचालित रूप से GitHub से नवीनतम संस्करण लाता है और चलाता है।

### पूर्वापेक्षाएँ

- आपके सिस्टम पर [uv](https://github.com/astral-sh/uv) स्थापित होना चाहिए।

### AI सहायकों के लिए सेटअप (जैसे Claude Desktop, Cline)

अपने AI सहायक की MCP कॉन्फ़िगरेशन फ़ाइल (जैसे `cline_mcp_settings.json` या `claude_desktop_config.json`) में निम्नलिखित जोड़ें:

> **विंडोज उपयोगकर्ताओं के लिए नोट**: कुछ डिपेंडेंसी के साथ संकलन (compilation) समस्याओं से बचने के लिए `--python 3.12` निर्दिष्ट करने की दृढ़ता से अनुशंसा की जाती है।

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

### महत्वपूर्ण: ब्राउज़र इंस्टालेशन

क्रॉलर डायनेमिक कंटेंट को संभालने के लिए Playwright का उपयोग करता है। टूल सेटअप करने के बाद आपको आवश्यक ब्राउज़र स्थापित करने होंगे:

```bash
uv run playwright install chromium
```

## 🖥️ उपयोग

एक बार कॉन्फ़िगर हो जाने पर, आप अपने AI सहायक से क्रॉल करने के लिए कहकर क्रॉलर का उपयोग कर सकते हैं।

### Claude/Cline के साथ उपयोग के उदाहरण

- **सरल क्रॉल**: "क्या आप example.com साइट को क्रॉल कर सकते हैं और मुझे सारांश दे सकते हैं?"
- **विकल्पों के साथ क्रॉल**: "क्या आप https://example.com को 3 की गहराई के साथ क्रॉल कर सकते हैं और बाहरी लिंक शामिल कर सकते हैं?"
- **डायनेमिक कंटेंट**: "इस React ऐप को क्रॉल करें और `.main-content` सिलेक्टर के लोड होने की प्रतीक्षा करें।"
- **सुरक्षा बायपास (Bypass Protections)**: "example.com को क्रॉल करें लेकिन एंटी-बॉट सुरक्षा को बायपास करने के लिए 'मैजिक मोड' का उपयोग करें।"
- **लक्षित निष्कर्षण (Targeted Extraction)**: "दस्तावेज़ साइट को क्रॉल करें लेकिन केवल `h1, p.lead` CSS सिलेक्टर से मेल खाने वाले कंटेंट को निकालें।"

## 🛠️ उपलब्ध पैरामीटर्स (MCP टूल)

`crawl` टूल निम्नलिखित पैरामीटर्स स्वीकार करता है:

| पैरामीटर | प्रकार | विवरण | डिफ़ॉल्ट मान |
|-----------|------|-------------|---------------|
| `url` | string | क्रॉल करने के लिए URL (आवश्यक) | - |
| `max_depth` | integer | अधिकतम क्रॉलिंग गहराई | 2 |
| `include_external` | boolean | बाहरी लिंक शामिल करें | false |
| `verbose` | boolean | विस्तृत आउटपुट सक्षम करें | true |
| `wait_for_selector` | string | कंटेंट निकालने से पहले प्रतीक्षा करने के लिए CSS सिलेक्टर। सिंगल-पेज एप्लिकेशन (SPA) के लिए उपयोगी। | None |
| `return_content` | boolean | क्या निकाला गया कंटेंट सीधे MCP रिस्पॉन्स में वापस करना है (यदि आवश्यक हो तो 50k वर्णों तक छोटा किया गया)। | true |
| `output_file` | string | आउटपुट फ़ाइल पथ | स्वचालित रूप से जनरेट किया गया |
| `magic` | boolean | एंटी-बॉट्स को बायपास करने और वास्तविक ब्राउज़र का अनुकरण करने के लिए मैजिक मोड सक्षम करें | false |
| `css_selector` | string | पृष्ठ से केवल लक्षित तत्वों को निकालने के लिए विशिष्ट CSS सिलेक्टर | None |
| `js_code` | string | निष्कर्षण से पहले पृष्ठ पर निष्पादित करने के लिए कस्टम जावास्क्रिप्ट कोड | None |
| `session_id` | string | अनुरोधों के बीच कुकीज़ और ब्राउज़र स्थिति को बनाए रखने के लिए स्थायी सत्र पहचानकर्ता | None |
| `delay_before_return_html` | number | HTML निकालने से पहले प्रतीक्षा करने के लिए सेकंड में देरी (भारी JS पृष्ठों के लिए उपयोगी) | None |

## 👨‍💻 विकास

यदि आप क्रॉलर को संशोधित करना चाहते हैं या इसे स्थानीय रूप से चलाना चाहते हैं:

1. इस रिपॉजिटरी को क्लोन करें:
```bash
git clone https://github.com/laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. `uv` का उपयोग करके डिपेंडेंसी स्थापित करें:
```bash
uv sync
```

3. आधिकारिक MCP इंस्पेक्टर का उपयोग करके स्थानीय रूप से MCP सर्वर का परीक्षण करें:
```bash
npx -y @modelcontextprotocol/inspector uv run crawl4ai-mcp
```

4. स्वचालित परीक्षण सूट चलाएँ:
```bash
uv run pytest tests/
```

5. सीधे MCP सर्वर चलाएँ (मानक उपयोग के लिए):
```bash
uv run crawl4ai-mcp
```

## 🤝 योगदान

योगदान का स्वागत है! बेझिझक एक समस्या (issue) खोलें या पुल अनुरोध (pull request) सबमिट करें।

## 📄 लाइसेंस

यह प्रोजेक्ट MIT लाइसेंस के तहत लाइसेंस प्राप्त है - विवरण के लिए LICENSE फ़ाइल देखें।
