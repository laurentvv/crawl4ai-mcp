# Web Crawler MCP

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Alat web crawling yang kuat yang terintegrasi dengan asisten AI melalui MCP (Machine Conversation Protocol). Proyek ini memungkinkan Anda untuk melakukan crawling situs web dan menyimpan kontennya [...]

## 📋 Fitur

- Crawling situs web dengan kedalaman yang dapat dikonfigurasi
- Dukungan untuk tautan internal dan eksternal
- Pembuatan file Markdown terstruktur
- Integrasi native dengan asisten AI melalui MCP
- Statistik hasil crawling yang detail
- Penanganan kesalahan dan halaman tidak ditemukan

## 🚀 Instalasi

### Prasyarat

- Python 3.9 atau lebih tinggi

### Langkah-langkah Instalasi

1. Klon repositori ini:

```bash
git clone laurentvv/crawl4ai-mcp
cd crawl4ai-mcp
```

2. Buat dan aktifkan lingkungan virtual:

```bash
# Windows
uv venv
source .venv/bin/activate

# Linux/MacOS
uv venv
source .venv/bin/activate
```

3. Pasang dependensi yang diperlukan:

```bash
uv sync
```

## 🔧 Konfigurasi

### Konfigurasi MCP untuk Asisten AI

Untuk menggunakan crawler ini dengan asisten AI seperti VScode Cline, konfigurasikan file `cline_mcp_settings.json` Anda:

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

Ganti `PATH\\TO\\YOUR\\ENVIRONMENT` dan `PATH\\TO\\YOUR\\PROJECT` dengan jalur yang sesuai di sistem Anda.

#### Contoh Konkret (Windows)

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

## 🖥️ Penggunaan

### Penggunaan dengan Asisten AI (melalui MCP)

Setelah dikonfigurasi di asisten AI Anda, Anda dapat menggunakan crawler dengan meminta asisten untuk melakukan crawling menggunakan sintaks berikut:

```
Bisakah Anda melakukan crawling situs web https://example.com dengan kedalaman 2?
```

Asisten akan menggunakan protokol MCP untuk menjalankan alat crawling dengan parameter yang ditentukan.

### Contoh Penggunaan dengan Claude

Berikut adalah contoh permintaan yang dapat Anda ajukan kepada Claude setelah mengonfigurasi alat MCP:

- **Crawling Sederhana**: "Bisakah Anda melakukan crawling situs example.com dan memberikan saya ringkasannya?"
- **Crawling dengan Opsi**: "Bisakah Anda melakukan crawling https://example.com dengan kedalaman 3 dan menyertakan tautan eksternal?"
- **Crawling dengan Output Kustom**: "Bisakah Anda melakukan crawling blog example.com dan menyimpan hasilnya dalam file bernama 'blog_analysis.md'?"

## 📁 Struktur Hasil

Hasil crawling disimpan di folder `crawl_results` di root proyek. Setiap file hasil dalam format Markdown dengan struktur berikut:

```markdown
# https://example.com/page

## Metadata
- Kedalaman: 1
- Timestamp: 2023-07-01T12:34:56

## Konten
Konten yang diekstrak dari halaman...

---
```

## 🛠️ Parameter yang Tersedia

Alat crawl menerima parameter berikut:

| Parameter | Tipe | Deskripsi | Nilai Default |
|-----------|------|-------------|---------------|
| url | string | URL untuk di-crawl (wajib) | - |
| max_depth | integer | Kedalaman crawling maksimum | 2 |
| include_external | boolean | Sertakan tautan eksternal | false |
| verbose | boolean | Aktifkan output detail | true |
| output_file | string | Jalur file output | dibuat otomatis |

## 📊 Format Hasil

Alat ini mengembalikan ringkasan dengan:
- URL yang di-crawl
- Jalur ke file yang dihasilkan
- Durasi crawling
- Statistik tentang halaman yang diproses (berhasil, gagal, tidak ditemukan, akses dilarang)

Hasil disimpan di direktori `crawl_results` proyek Anda.

## 🤝 Kontribusi

Kontribusi dipersilakan! Jangan ragu untuk membuka issue atau mengirimkan pull request.

## 📄 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file LICENSE untuk detail.