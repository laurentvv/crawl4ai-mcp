# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Alat perayapan web (web crawling) canggih yang terintegrasi dengan asisten AI melalui MCP (Model Context Protocol). Proyek ini memungkinkan asisten AI untuk merayapi situs web, mengekstrak konten dinamis, menavigasi melalui tautan, dan menyimpan file Markdown terstruktur secara langsung.

## 📋 Fitur

- Integrasi asli dengan asisten AI melalui MCP
- Mengembalikan konten Markdown hasil scraping langsung ke AI
- Mengekstrak dan menampilkan tautan internal/eksternal untuk navigasi AI
- Menunggu pemilih (selector) CSS dinamis sebelum scraping (dukungan SPA)
- Perayapan situs web dengan kedalaman yang dapat dikonfigurasi
- Statistik hasil perayapan yang mendalam
- Penanganan kesalahan dan halaman tidak ditemukan

## 🚀 Konfigurasi MCP

Cara termudah dan yang direkomendasikan untuk menggunakan alat ini adalah melalui `uvx`, yang secara otomatis mengambil dan menjalankan versi terbaru dari GitHub tanpa mengharuskan Anda untuk mengkloning repositori secara manual.

### Prasyarat

- [uv](https://github.com/astral-sh/uv) terinstal di sistem Anda.

### Penyiapan untuk Asisten AI (misalnya, Claude Desktop, Cline)

Tambahkan berikut ini ke file konfigurasi MCP Asisten AI Anda (misalnya, `cline_mcp_settings.json` atau `claude_desktop_config.json`):

> **Catatan untuk Pengguna Windows**: Sangat disarankan untuk menentukan `--python 3.12` untuk menghindari masalah kompilasi dengan dependensi tertentu.

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

### Penting: Instalasi Browser

Perayap menggunakan Playwright untuk menangani konten dinamis. Anda harus menginstal browser yang diperlukan setelah menyiapkan alat:

```bash
uv run playwright install chromium
```

## 🖥️ Penggunaan

Setelah dikonfigurasi, Anda dapat menggunakan perayap dengan meminta asisten AI Anda untuk melakukan perayapan.

### Contoh Penggunaan dengan Claude/Cline

- **Perayapan Sederhana**: "Bisakah kamu merayapi situs example.com dan memberi saya ringkasannya?"
- **Perayapan dengan Opsi**: "Bisakah kamu merayapi https://example.com dengan kedalaman 3 dan sertakan tautan eksternal?"
- **Konten Dinamis**: "Rayapi aplikasi React ini dan tunggu pemilih `.main-content` dimuat."

## 🛠️ Parameter yang Tersedia (Alat MCP)

Alat `crawl` menerima parameter berikut:

| Parameter | Tipe | Deskripsi | Nilai Default |
|-----------|------|-------------|---------------|
| `url` | string | URL untuk dirayapi (diperlukan) | - |
| `max_depth` | integer | Kedalaman perayapan maksimum | 2 |
| `include_external` | boolean | Sertakan tautan eksternal | false |
| `verbose` | boolean | Aktifkan output mendalam | true |
| `wait_for_selector` | string | Pemilih CSS untuk ditunggu sebelum mengekstrak konten. Berguna untuk aplikasi satu halaman (SPA). | None |
| `return_content` | boolean | Apakah akan mengembalikan konten yang diekstrak langsung dalam respons MCP (dipotong menjadi 50rb karakter jika perlu). | true |
| `output_file` | string | Jalur file output | dibuat secara otomatis |

## 👨‍💻 Pengembangan

Jika Anda ingin memodifikasi perayap atau menjalankannya secara lokal:

1. Kloning repositori ini:
```bash
git clone https://github.com/laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Instal dependensi menggunakan `uv`:
```bash
uv sync
```

3. Jalankan server MCP secara langsung:
```bash
uv run crawl4ai-mcp
```

## 🤝 Kontribusi

Kontribusi sangat diterima! Jangan ragu untuk membuka issue atau mengirimkan pull request.

## 📄 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file LICENSE untuk detailnya.
