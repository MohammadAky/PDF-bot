"""
User State Management
"""

from typing import Dict, List, Any, Optional
from config.settings import DEFAULT_LANGUAGE


# Global state storage
user_languages: Dict[int, str] = {}
user_states: Dict[int, str] = {}
user_files: Dict[int, List[str]] = {}
user_temp_data: Dict[int, Dict[str, Any]] = {}


def get_user_language(user_id: int) -> str:
    """Get user's preferred language"""
    return user_languages.get(user_id, DEFAULT_LANGUAGE)


def set_user_language(user_id: int, language: str) -> None:
    """Set user's preferred language"""
    user_languages[user_id] = language


class UserStateManager:
    """Manage user states and data"""
    
    @staticmethod
    def get_state(user_id: int) -> Optional[str]:
        """Get current state for user"""
        return user_states.get(user_id)
    
    @staticmethod
    def set_state(user_id: int, state: str) -> None:
        """Set state for user"""
        user_states[user_id] = state
    
    @staticmethod
    def clear_state(user_id: int) -> None:
        """Clear state for user"""
        if user_id in user_states:
            del user_states[user_id]
    
    @staticmethod
    def get_files(user_id: int) -> List[str]:
        """Get list of files for user"""
        return user_files.get(user_id, [])
    
    @staticmethod
    def add_file(user_id: int, file_path: str) -> None:
        """Add file to user's file list"""
        if user_id not in user_files:
            user_files[user_id] = []
        user_files[user_id].append(file_path)
    
    @staticmethod
    def clear_files(user_id: int) -> None:
        """Clear all files for user"""
        if user_id in user_files:
            user_files[user_id] = []
    
    @staticmethod
    def get_temp(user_id: int, key: str) -> Any:
        """Get temporary data for user"""
        if user_id not in user_temp_data:
            return None
        return user_temp_data[user_id].get(key)
    
    @staticmethod
    def set_temp(user_id: int, key: str, value: Any) -> None:
        """Set temporary data for user"""
        if user_id not in user_temp_data:
            user_temp_data[user_id] = {}
        user_temp_data[user_id][key] = value
    
    @staticmethod
    def clear_temp(user_id: int) -> None:
        """Clear all temporary data for user"""
        if user_id in user_temp_data:
            del user_temp_data[user_id]
    
    @staticmethod
    def clear_all(user_id: int) -> None:
        """Clear all data for user"""
        UserStateManager.clear_state(user_id)
        UserStateManager.clear_files(user_id)
        UserStateManager.clear_temp(user_id)


# State constants
class States:
    """State constants"""
    # Organize
    MERGING = "merging"
    SPLITTING = "splitting"
    EXTRACTING_PAGES = "extracting_pages"
    EXTRACTING_PAGES_WAIT_SPEC = "extracting_pages_wait_spec"
    REMOVING_PAGES = "removing_pages"
    REMOVING_PAGES_WAIT_SPEC = "removing_pages_wait_spec"
    EXTRACTING_IMAGES = "extracting_images"
    EXTRACTING_TEXT = "extracting_text"
    
    # Optimize
    COMPRESSING = "compressing"
    COMPRESSING_WAIT_LEVEL = "compressing_wait_level"
    REPAIRING = "repairing"
    OCR_PROCESSING = "ocr_processing"
    
    # Convert
    COLLECTING_IMAGES = "collecting_images"
    WORD_TO_PDF = "word_to_pdf"
    EXCEL_TO_PDF = "excel_to_pdf"
    POWERPOINT_TO_PDF = "powerpoint_to_pdf"
    PDF_TO_JPG = "pdf_to_jpg"
    PDF_TO_WORD = "pdf_to_word"
    
    # Edit
    ROTATING = "rotating"
    ROTATING_WAIT_ANGLE = "rotating_wait_angle"
    ADDING_PAGE_NUMBERS = "adding_page_numbers"
    ADDING_WATERMARK = "adding_watermark"
    CROPPING = "cropping"
    
    # Security
    UNLOCKING = "unlocking"
    UNLOCKING_WAIT_PASSWORD = "unlocking_wait_password"
    PROTECTING = "protecting"
    PROTECTING_WAIT_PASSWORD = "protecting_wait_password"