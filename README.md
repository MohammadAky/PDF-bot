# 📄 PDF Bot - Complete PDF Management Solution

A powerful Telegram bot that provides comprehensive PDF operations including conversion, editing, merging, optimization, and security features. Supports both English and Persian (فارسی) languages.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-20.7-blue.svg)](https://github.com/python-telegram-bot/python-telegram-bot)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

### 📑 Organize PDF

- **Merge PDFs** - Combine multiple PDF files into one
- **Split PDF** - Split PDFs by page ranges, every N pages, or specific pages
- **Extract Pages** - Extract specific pages from a PDF
- **Remove Pages** - Remove unwanted pages from a PDF
- **Reorder Pages** - Rearrange pages in any order
- **Extract Images** - Extract all images from a PDF
- **Extract Text** - Extract all text content from a PDF

### ⚡ Optimize PDF

- **Compress PDF** - Reduce file size with quality options (low/medium/high)
- **Repair PDF** - Fix corrupted or damaged PDF files
- **OCR PDF** - Convert scanned documents to searchable PDFs
- **Optimize Images** - Compress images within PDFs
- **Remove Metadata** - Strip metadata for privacy

### 🔄 Convert PDF

- **Images to PDF** - Convert JPG, PNG, WEBP, BMP, TIFF to PDF
- **PDF to Images** - Convert PDF pages to JPG/PNG images
- **Word to PDF** - Convert DOCX, DOC to PDF
- **PDF to Word** - Convert PDF to editable Word documents
- **Excel to PDF** - Convert XLSX, XLS, CSV to PDF
- **PDF to Excel** - Extract tables to Excel format
- **PowerPoint to PDF** - Convert PPTX, PPT to PDF
- **PDF to PowerPoint** - Convert PDF to editable presentations
- **HTML to PDF** - Convert web pages to PDF
- **Text to PDF** - Convert plain text files to PDF
- **PDF to Text** - Extract text to TXT file

### ✏️ Edit PDF

- **Rotate PDF** - Rotate pages by 90°, 180°, or 270°
- **Add Page Numbers** - Add page numbers to all pages
- **Add Watermark** - Add image or text watermarks
- **Add Header/Footer** - Add custom headers and footers
- **Crop PDF** - Crop pages to specific dimensions
- **Resize PDF** - Change page size (A4, Letter, etc.)
- **Black & White** - Convert PDF to grayscale
- **Adjust Margins** - Modify page margins

### 🔒 PDF Security

- **Unlock PDF** - Remove password protection
- **Protect PDF** - Add password protection
- **Sign PDF** - Digitally sign documents (coming soon)
- **Redact PDF** - Permanently remove sensitive information (coming soon)
- **Compare PDFs** - Compare two PDF files (coming soon)
- **Add Permissions** - Set printing, copying restrictions
- **Remove Metadata** - Strip all metadata

### 🌐 Language Support

- **English** - Full support
- **Persian (فارسی)** - Full RTL support

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Tesseract OCR (optional, for OCR features)
- wkhtmltopdf (optional, for HTML to PDF)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/MohammadAky/PDF-bot.git
cd PDF-bot
```

2. **Set up project structure**

```bash
python setup_structure.py
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env and add your BOT_TOKEN
```

5. **Run the bot**

```bash
python main.py
```

## 📁 Project Structure

```
PDF-bot/
├── bot/
│   ├── __init__.py
│   ├── handlers.py          # Message and command handlers
│   ├── callbacks.py         # Button callback handlers
│   ├── keyboards.py         # Keyboard layouts
│   └── states.py            # User state management
├── services/
│   ├── __init__.py
│   ├── pdf_converter.py     # PDF conversion services
│   ├── pdf_organizer.py     # Merge, split, extract, remove
│   ├── pdf_optimizer.py     # Compress, repair, OCR
│   ├── pdf_editor.py        # Rotate, watermark, page numbers
│   ├── pdf_security.py      # Lock, unlock, sign, redact
│   └── image_processor.py   # Image handling
├── utils/
│   ├── __init__.py
│   ├── file_manager.py      # File operations
│   ├── language_manager.py  # Language handling
│   ├── subscriber_manager.py # Subscriber management
│   ├── logger.py            # Logging utilities
│   └── validators.py        # Input validation
├── config/
│   ├── __init__.py
│   ├── settings.py          # Configuration settings
│   └── texts.py             # Multilingual texts
├── temp/                    # Temporary files
├── logs/                    # Log files
├── data/                    # User data and stats
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789,987654321
SUPPORT_USERNAME=YourSupportUsername

# File Limits
MAX_FILE_SIZE_MB=50
MAX_IMAGES_PER_PDF=100
MAX_PDFS_TO_MERGE=20

# Feature Flags
OCR_ENABLED=true
PDF_TO_WORD_ENABLED=true
PDF_TO_EXCEL_ENABLED=true

# OCR Configuration
OCR_LANGUAGE=eng
OCR_TIMEOUT=300

# Rate Limiting
MAX_OPERATIONS_PER_HOUR=50
RATE_LIMIT_ENABLED=false
```

### Feature Configuration

Edit `config/settings.py` to enable/disable features:

```python
FEATURES = {
    "merge": True,
    "split": True,
    "compress": True,
    "rotate": True,
    "watermark": True,
    "ocr": True,
    # ... more features
}
```

## 📝 Usage

### Basic Commands

- `/start` - Start the bot and choose language
- `/help` - Show help message with all features
- `/language` - Change language (English/Persian)
- `/cancel` - Cancel current operation
- `/subscribe` - Subscribe to feature updates
- `/unsubscribe` - Unsubscribe from updates

### Example Workflows

#### Merge PDFs

1. Click "📑 Organize PDF"
2. Click "🔗 Merge PDFs"
3. Send multiple PDF files
4. Click "Merge Now" when done

#### Convert Images to PDF

1. Click "🔄 Convert PDF"
2. Click "🖼️ JPG to PDF"
3. Send multiple images
4. Click "Done" to create PDF

#### Compress PDF

1. Click "⚡ Optimize PDF"
2. Click "🗜️ Compress PDF"
3. Send a PDF file
4. Choose compression level (1, 2, or 3)

#### Add Watermark

1. Click "✏️ Edit PDF"
2. Click "💧 Add Watermark"
3. Send a PDF file
4. Send a watermark image

## 🛠️ Development

### Adding New Features

1. **Create service function** in appropriate service file
2. **Add text translations** in `config/texts.py`
3. **Create callback handler** in `bot/callbacks.py`
4. **Add keyboard button** in `bot/keyboards.py`
5. **Update feature flag** in `config/settings.py`

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black .
flake8 .
```

## 🔧 Advanced Features

### OCR Configuration

Install Tesseract OCR:

**Ubuntu/Debian:**

```bash
sudo apt-get install tesseract-ocr
```

**macOS:**

```bash
brew install tesseract
```

**Windows:**
Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

### HTML to PDF

Install wkhtmltopdf:

**Ubuntu/Debian:**

```bash
sudo apt-get install wkhtmltopdf
```

**macOS:**

```bash
brew install wkhtmltopdf
```

## 📊 Statistics & Analytics

Track user statistics:

- Total PDFs processed
- Images converted
- Files merged
- Most used features

Access stats: `/stats` (admin only)

## 🔐 Security

- All temporary files are automatically deleted
- Password-protected operations use secure encryption
- No user data is stored permanently (except subscribers list)
- Rate limiting to prevent abuse

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [PyPDF2](https://github.com/py-pdf/pypdf2) - PDF processing
- [Pillow](https://github.com/python-pillow/Pillow) - Image processing
- [Tesseract](https://github.com/tesseract-ocr/tesseract) - OCR engine

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/MohammadAky/PDF-bot/issues)
- **Telegram**: [@YourSupportUsername](https://t.me/YourSupportUsername)
- **Email**: your.email@example.com

## 🗺️ Roadmap

### ✅ Implemented

- [x] Basic PDF operations (merge, split, rotate)
- [x] Image to PDF conversion
- [x] PDF compression
- [x] Password protection
- [x] Page extraction and removal
- [x] Watermarks and page numbers
- [x] Bilingual support (EN/FA)
- [x] Extract images and text

### 🚧 Coming Soon

- [ ] Digital signatures
- [ ] PDF redaction
- [ ] PDF comparison tool
- [ ] Advanced OCR with multiple languages
- [ ] Batch processing
- [ ] Cloud storage integration (Google Drive, Dropbox)
- [ ] PDF form filling
- [ ] PDF to ePub conversion
- [ ] Schedule documents
- [ ] Collaborative editing

### 💡 Future Ideas

- [ ] Web interface
- [ ] API access
- [ ] Mobile app
- [ ] AI-powered features
- [ ] Document templates
- [ ] Workflow automation

## 📈 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## 💻 System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **RAM**: Minimum 512MB, recommended 1GB+
- **Disk Space**: 500MB for bot + dependencies
- **Network**: Stable internet connection for Telegram API

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MohammadAky/PDF-bot&type=Date)](https://star-history.com/#MohammadAky/PDF-bot&Date)

---

**Made with ❤️ by [MohammadAky](https://github.com/MohammadAky)**

If you find this bot useful, please consider giving it a ⭐ on GitHub!
