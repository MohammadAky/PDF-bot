"""
Configuration settings for the PDF Bot
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "YourSupportUsername")

# File Settings
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
MAX_IMAGES_PER_PDF = int(os.getenv("MAX_IMAGES_PER_PDF", "100"))
MAX_PDFS_TO_MERGE = int(os.getenv("MAX_PDFS_TO_MERGE", "20"))

# Directory Settings
TEMP_DIR = BASE_DIR / "temp"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"

# Create directories if they don't exist
for directory in [TEMP_DIR, LOGS_DIR, DATA_DIR]:
    directory.mkdir(exist_ok=True)

# File paths
SUBSCRIBERS_FILE = DATA_DIR / "subscribers.json"
USER_STATS_FILE = DATA_DIR / "user_stats.json"
LOG_FILE = LOGS_DIR / "bot.log"

# Language Settings
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ["en", "fa"]

# PDF Processing Settings
PDF_QUALITY = {
    "low": 50,
    "medium": 75,
    "high": 90
}

# Compression levels
COMPRESSION_LEVELS = {
    1: "low",
    2: "medium",
    3: "high"
}

# Image settings
IMAGE_DPI = 300
IMAGE_QUALITY = 95
SUPPORTED_IMAGE_FORMATS = ["jpg", "jpeg", "png", "webp", "bmp", "tiff"]

# Document settings
SUPPORTED_DOCUMENT_FORMATS = ["docx", "doc", "txt", "rtf", "odt"]
SUPPORTED_SPREADSHEET_FORMATS = ["xlsx", "xls", "csv"]
SUPPORTED_PRESENTATION_FORMATS = ["pptx", "ppt", "odp"]

# OCR Settings
OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "eng")  # Tesseract language code
OCR_TIMEOUT = int(os.getenv("OCR_TIMEOUT", "300"))  # 5 minutes

# Security Settings
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 128

# Rate Limiting
MAX_OPERATIONS_PER_HOUR = int(os.getenv("MAX_OPERATIONS_PER_HOUR", "50"))
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true"

# Feature Flags
FEATURES = {
    "merge": True,
    "split": True,
    "compress": True,
    "rotate": True,
    "watermark": True,
    "page_numbers": True,
    "extract_pages": True,
    "remove_pages": True,
    "extract_images": True,
    "extract_text": True,
    "unlock": True,
    "protect": True,
    "repair": True,
    "ocr": os.getenv("OCR_ENABLED", "false").lower() == "true",
    "pdf_to_word": os.getenv("PDF_TO_WORD_ENABLED", "false").lower() == "true",
    "pdf_to_excel": os.getenv("PDF_TO_EXCEL_ENABLED", "false").lower() == "true",
    "sign": False,  # Coming soon
    "redact": False,  # Coming soon
    "compare": False,  # Coming soon
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": str(LOG_FILE),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf-8"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
}

# Validation
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")