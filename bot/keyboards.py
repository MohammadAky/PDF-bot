"""
Keyboard Layouts for the Bot
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config.texts import get_text
from bot.states import get_user_language


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_main_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Main menu keyboard"""
    lang = get_user_language(user_id)
    keyboard = [
        [InlineKeyboardButton(get_text(lang, "organize_pdf"), callback_data="menu_organize")],
        [InlineKeyboardButton(get_text(lang, "optimize_pdf"), callback_data="menu_optimize")],
        [InlineKeyboardButton(get_text(lang, "convert_pdf"), callback_data="menu_convert")],
        [InlineKeyboardButton(get_text(lang, "edit_pdf"), callback_data="menu_edit")],
        [InlineKeyboardButton(get_text(lang, "pdf_security"), callback_data="menu_security")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_organize_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Organize PDF menu keyboard"""
    lang = get_user_language(user_id)
    keyboard = [
        [InlineKeyboardButton(get_text(lang, "merge_pdfs"), callback_data="merge")],
        [InlineKeyboardButton(get_text(lang, "split_pdf"), callback_data="split")],
        [InlineKeyboardButton(get_text(lang, "extract_pages"), callback_data="extract_pages")],
        [InlineKeyboardButton(get_text(lang, "remove_pages"), callback_data="remove_pages")],
        [
            InlineKeyboardButton(get_text(lang, "extract_images"), callback_data="extract_images"),
            InlineKeyboardButton(get_text(lang, "extract_text"), callback_data="extract_text")
        ],
        [InlineKeyboardButton(get_text(lang, "back"), callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_optimize_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Optimize PDF menu keyboard"""
    lang = get_user_language(user_id)
    keyboard = [
        [InlineKeyboardButton(get_text(lang, "compress_pdf"), callback_data="compress")],
        [InlineKeyboardButton(get_text(lang, "repair_pdf"), callback_data="repair")],
        [InlineKeyboardButton(get_text(lang, "ocr_pdf"), callback_data="ocr")],
        [InlineKeyboardButton(get_text(lang, "back"), callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_convert_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Convert PDF menu keyboard"""
    lang = get_user_language(user_id)
    keyboard = [
        [
            InlineKeyboardButton(get_text(lang, "jpg_to_pdf"), callback_data="jpg_to_pdf"),
            InlineKeyboardButton(get_text(lang, "pdf_to_jpg"), callback_data="pdf_to_jpg")
        ],
        [
            InlineKeyboardButton(get_text(lang, "word_to_pdf"), callback_data="word_to_pdf"),
            InlineKeyboardButton(get_text(lang, "pdf_to_word"), callback_data="pdf_to_word")
        ],
        [
            InlineKeyboardButton(get_text(lang, "excel_to_pdf"), callback_data="excel_to_pdf"),
            InlineKeyboardButton(get_text(lang, "powerpoint_to_pdf"), callback_data="powerpoint_to_pdf")
        ],
        [InlineKeyboardButton(get_text(lang, "back"), callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_edit_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Edit PDF menu keyboard"""
    lang = get_user_language(user_id)
    keyboard = [
        [InlineKeyboardButton(get_text(lang, "rotate_pdf"), callback_data="rotate")],
        [InlineKeyboardButton(get_text(lang, "add_page_numbers"), callback_data="add_page_numbers")],
        [InlineKeyboardButton(get_text(lang, "add_watermark"), callback_data="watermark")],
        [InlineKeyboardButton(get_text(lang, "crop_pdf"), callback_data="crop")],
        [InlineKeyboardButton(get_text(lang, "back"), callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_security_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """PDF security menu keyboard"""
    lang = get_user_language(user_id)
    keyboard = [
        [
            InlineKeyboardButton(get_text(lang, "unlock_pdf"), callback_data="unlock"),
            InlineKeyboardButton(get_text(lang, "protect_pdf"), callback_data="protect")
        ],
        [InlineKeyboardButton(get_text(lang, "sign_pdf"), callback_data="sign")],
        [InlineKeyboardButton(get_text(lang, "redact_pdf"), callback_data="redact")],
        [InlineKeyboardButton(get_text(lang, "compare_pdf"), callback_data="compare")],
        [InlineKeyboardButton(get_text(lang, "back"), callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Simple back button keyboard"""
    lang = get_user_language(user_id)
    keyboard = [
        [InlineKeyboardButton(get_text(lang, "back"), callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_cancel_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Cancel button keyboard"""
    lang = get_user_language(user_id)
    keyboard = [
        [InlineKeyboardButton(get_text(lang, "cancel"), callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_done_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Done and cancel keyboard"""
    lang = get_user_language(user_id)
    keyboard = [
        [InlineKeyboardButton(get_text(lang, "done"), callback_data="create_pdf_from_images")],
        [InlineKeyboardButton(get_text(lang, "cancel"), callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_merge_keyboard(user_id: int, count: int) -> InlineKeyboardMarkup:
    """Merge PDFs keyboard with file count"""
    lang = get_user_language(user_id)
    keyboard = [
        [InlineKeyboardButton(
            get_text(lang, "merge_now") + f" ({count} files)",
            callback_data="do_merge"
        )],
        [InlineKeyboardButton(get_text(lang, "cancel"), callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)