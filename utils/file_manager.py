"""
File Management Utilities
"""

import os
import logging
from typing import List
from config.settings import TEMP_DIR, MAX_FILE_SIZE_MB

logger = logging.getLogger(__name__)


async def download_file(bot, file_id: str, filename: str) -> str:
    """
    Download a file from Telegram
    
    Args:
        bot: Telegram bot instance
        file_id: File ID from Telegram
        filename: Name to save file as
        
    Returns:
        Path to downloaded file
    """
    try:
        file = await bot.get_file(file_id)
        file_path = os.path.join(TEMP_DIR, filename)
        
        # Ensure temp directory exists
        os.makedirs(TEMP_DIR, exist_ok=True)
        
        await file.download_to_drive(file_path)
        logger.info(f"File downloaded: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise


def cleanup_files(file_paths: List[str]) -> None:
    """
    Delete temporary files
    
    Args:
        file_paths: List of file paths to delete
    """
    for file_path in file_paths:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up file {file_path}: {e}")


def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in bytes
    """
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        logger.error(f"Error getting file size: {e}")
        return 0


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in MB
    """
    size_bytes = get_file_size(file_path)
    return size_bytes / (1024 * 1024)


def is_file_too_large(file_path: str, max_size_mb: int = MAX_FILE_SIZE_MB) -> bool:
    """
    Check if file is too large
    
    Args:
        file_path: Path to file
        max_size_mb: Maximum size in MB
        
    Returns:
        True if file is too large
    """
    size_mb = get_file_size_mb(file_path)
    return size_mb > max_size_mb


def ensure_directory(directory: str) -> None:
    """
    Ensure directory exists
    
    Args:
        directory: Directory path
    """
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}")


def cleanup_temp_directory(max_age_hours: int = 24) -> None:
    """
    Clean up old files from temp directory
    
    Args:
        max_age_hours: Maximum age of files to keep in hours
    """
    import time
    
    try:
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                
                if file_age > max_age_seconds:
                    os.remove(file_path)
                    logger.info(f"Cleaned up old file: {file_path}")
                    
    except Exception as e:
        logger.error(f"Error cleaning temp directory: {e}")


def get_file_extension(file_path: str) -> str:
    """
    Get file extension
    
    Args:
        file_path: Path to file
        
    Returns:
        File extension (lowercase, without dot)
    """
    return os.path.splitext(file_path)[1][1:].lower()


def is_pdf(file_path: str) -> bool:
    """
    Check if file is a PDF
    
    Args:
        file_path: Path to file
        
    Returns:
        True if file is PDF
    """
    return get_file_extension(file_path) == "pdf"


def is_image(file_path: str) -> bool:
    """
    Check if file is an image
    
    Args:
        file_path: Path to file
        
    Returns:
        True if file is an image
    """
    image_extensions = ["jpg", "jpeg", "png", "webp", "bmp", "tiff", "gif"]
    return get_file_extension(file_path) in image_extensions


def is_document(file_path: str) -> bool:
    """
    Check if file is a document
    
    Args:
        file_path: Path to file
        
    Returns:
        True if file is a document
    """
    doc_extensions = ["docx", "doc", "txt", "rtf", "odt"]
    return get_file_extension(file_path) in doc_extensions


def generate_unique_filename(base_name: str, extension: str) -> str:
    """
    Generate unique filename
    
    Args:
        base_name: Base name for file
        extension: File extension
        
    Returns:
        Unique filename
    """
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return f"{base_name}_{unique_id}.{extension}"


def get_safe_filename(filename: str) -> str:
    """
    Get safe filename (remove special characters)
    
    Args:
        filename: Original filename
        
    Returns:
        Safe filename
    """
    import re
    # Remove special characters
    safe_name = re.sub(r'[^\w\s\-\.]', '', filename)
    # Replace spaces with underscores
    safe_name = safe_name.replace(' ', '_')
    return safe_name