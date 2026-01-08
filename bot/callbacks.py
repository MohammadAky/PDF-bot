"""
Button Callback Handlers
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from config.texts import get_text
from bot.keyboards import *
from bot.states import UserStateManager, set_user_language, get_user_language
from utils.subscriber_manager import add_subscriber, remove_subscriber, is_subscribed
from utils.file_manager import cleanup_files, get_file_size_mb
from services.pdf_organizer import merge_pdfs
from services.image_processor import images_to_pdf

logger = logging.getLogger(__name__)
state_manager = UserStateManager()


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    data = query.data
    lang = get_user_language(user_id)
    
    logger.info(f"User {user_id} clicked button: {data}")
    
    # Language selection
    if data.startswith("lang_"):
        await handle_language_selection(query, user_id, data)
        return
    
    # Navigation
    if data == "back_to_menu":
        state_manager.clear_state(user_id)
        await query.edit_message_text(
            get_text(lang, "choose_action"),
            reply_markup=get_main_keyboard(user_id)
        )
        return
    
    # Main menu categories
    if data == "menu_organize":
        await query.edit_message_text(
            get_text(lang, "choose_action"),
            reply_markup=get_organize_keyboard(user_id)
        )
        return
    
    if data == "menu_optimize":
        await query.edit_message_text(
            get_text(lang, "choose_action"),
            reply_markup=get_optimize_keyboard(user_id)
        )
        return
    
    if data == "menu_convert":
        await query.edit_message_text(
            get_text(lang, "choose_action"),
            reply_markup=get_convert_keyboard(user_id)
        )
        return
    
    if data == "menu_edit":
        await query.edit_message_text(
            get_text(lang, "choose_action"),
            reply_markup=get_edit_keyboard(user_id)
        )
        return
    
    if data == "menu_security":
        await query.edit_message_text(
            get_text(lang, "choose_action"),
            reply_markup=get_security_keyboard(user_id)
        )
        return
    
    # Organize PDF operations
    if data == "merge":
        await handle_merge_start(query, user_id, lang)
        return
    
    if data == "do_merge":
        await handle_do_merge(query, user_id, lang, context)
        return
    
    if data == "split":
        await handle_split_start(query, user_id, lang)
        return
    
    if data == "extract_pages":
        await handle_extract_pages_start(query, user_id, lang)
        return
    
    if data == "remove_pages":
        await handle_remove_pages_start(query, user_id, lang)
        return
    
    if data == "extract_images":
        await handle_extract_images_start(query, user_id, lang)
        return
    
    if data == "extract_text":
        await handle_extract_text_start(query, user_id, lang)
        return
    
    # Optimize PDF operations
    if data == "compress":
        await handle_compress_start(query, user_id, lang)
        return
    
    if data == "repair":
        await handle_repair_start(query, user_id, lang)
        return
    
    if data == "ocr":
        await handle_ocr_start(query, user_id, lang)
        return
    
    # Convert PDF operations
    if data in ["jpg_to_pdf", "png_to_pdf", "convert"]:
        await handle_images_to_pdf_start(query, user_id, lang)
        return
    
    if data == "create_pdf_from_images":
        await handle_create_pdf_from_images(query, user_id, lang, context)
        return
    
    if data == "word_to_pdf":
        await handle_word_to_pdf_start(query, user_id, lang)
        return
    
    if data == "excel_to_pdf":
        await handle_excel_to_pdf_start(query, user_id, lang)
        return
    
    if data == "powerpoint_to_pdf":
        await handle_powerpoint_to_pdf_start(query, user_id, lang)
        return
    
    if data == "pdf_to_jpg":
        await handle_pdf_to_jpg_start(query, user_id, lang)
        return
    
    if data == "pdf_to_word":
        await handle_pdf_to_word_start(query, user_id, lang)
        return
    
    # Edit PDF operations
    if data == "rotate":
        await handle_rotate_start(query, user_id, lang)
        return
    
    if data == "add_page_numbers":
        await handle_page_numbers_start(query, user_id, lang)
        return
    
    if data == "watermark":
        await handle_watermark_start(query, user_id, lang)
        return
    
    # Security operations
    if data == "unlock":
        await handle_unlock_start(query, user_id, lang)
        return
    
    if data == "protect":
        await handle_protect_start(query, user_id, lang)
        return
    
    # Subscription management
    if data == "subscribe_coming":
        if not is_subscribed(user_id):
            add_subscriber(user_id)
            await query.edit_message_text(
                f"✅ {get_text(lang, 'subscribed')}\n\n{get_text(lang, 'coming_soon')}",
                reply_markup=get_back_keyboard(user_id)
            )
        else:
            await query.edit_message_text(
                f"✅ {get_text(lang, 'already_subscribed')}",
                reply_markup=get_back_keyboard(user_id)
            )
        return
    
    if data == "unsubscribe_coming":
        if is_subscribed(user_id):
            remove_subscriber(user_id)
            await query.edit_message_text(
                f"🔕 {get_text(lang, 'unsubscribed')}",
                reply_markup=get_back_keyboard(user_id)
            )
        else:
            await query.edit_message_text(
                f"ℹ️ {get_text(lang, 'not_subscribed')}",
                reply_markup=get_back_keyboard(user_id)
            )
        return
    
    # Coming soon features
    await handle_coming_soon(query, user_id, lang, data)


async def handle_language_selection(query, user_id: int, data: str) -> None:
    """Handle language selection"""
    lang_code = data.split("_")[1]
    set_user_language(user_id, lang_code)
    
    await query.edit_message_text(
        get_text(lang_code, "language_changed"),
        reply_markup=get_main_keyboard(user_id)
    )


async def handle_merge_start(query, user_id: int, lang: str) -> None:
    """Start PDF merging"""
    state_manager.set_state(user_id, "merging")
    state_manager.clear_files(user_id)
    
    await query.edit_message_text(
        get_text(lang, "send_pdfs"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_do_merge(query, user_id: int, lang: str, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Execute PDF merging"""
    files = state_manager.get_files(user_id)
    
    if len(files) < 2:
        await query.edit_message_text(
            get_text(lang, "no_pdfs"),
            reply_markup=get_main_keyboard(user_id)
        )
        return
    
    await query.edit_message_text(
        get_text(lang, "merging_pdfs", count=len(files))
    )
    
    try:
        output_path = await merge_pdfs(files)
        
        # Get file info
        from PyPDF2 import PdfReader
        reader = PdfReader(output_path)
        total_pages = len(reader.pages)
        file_size = get_file_size_mb(output_path)
        
        await context.bot.send_document(
            chat_id=user_id,
            document=open(output_path, 'rb'),
            filename="merged.pdf",
            caption=get_text(lang, "pdfs_merged",
                           pages=total_pages,
                           size=f"{file_size:.2f}MB")
        )
        
        await context.bot.send_message(
            chat_id=user_id,
            text=get_text(lang, "success"),
            reply_markup=get_main_keyboard(user_id)
        )
        
        cleanup_files(files + [output_path])
        state_manager.clear_state(user_id)
        state_manager.clear_files(user_id)
        
    except Exception as e:
        logger.error(f"Merge error: {e}", exc_info=True)
        await context.bot.send_message(
            chat_id=user_id,
            text=get_text(lang, "error"),
            reply_markup=get_main_keyboard(user_id)
        )


async def handle_split_start(query, user_id: int, lang: str) -> None:
    """Start PDF splitting"""
    state_manager.set_state(user_id, "splitting")
    
    await query.edit_message_text(
        get_text(lang, "send_pdf_for_split"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_extract_pages_start(query, user_id: int, lang: str) -> None:
    """Start page extraction"""
    state_manager.set_state(user_id, "extracting_pages")
    
    await query.edit_message_text(
        get_text(lang, "send_pdf_for_extract_pages"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_remove_pages_start(query, user_id: int, lang: str) -> None:
    """Start page removal"""
    state_manager.set_state(user_id, "removing_pages")
    
    await query.edit_message_text(
        get_text(lang, "send_pdf_for_remove_pages"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_extract_images_start(query, user_id: int, lang: str) -> None:
    """Start image extraction"""
    state_manager.set_state(user_id, "extracting_images")
    
    await query.edit_message_text(
        get_text(lang, "send_pdf_for_extract_images"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_extract_text_start(query, user_id: int, lang: str) -> None:
    """Start text extraction"""
    state_manager.set_state(user_id, "extracting_text")
    
    await query.edit_message_text(
        get_text(lang, "send_pdf_for_extract_text"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_compress_start(query, user_id: int, lang: str) -> None:
    """Start PDF compression"""
    state_manager.set_state(user_id, "compressing")
    
    await query.edit_message_text(
        get_text(lang, "send_pdf_for_compress"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_repair_start(query, user_id: int, lang: str) -> None:
    """Start PDF repair"""
    state_manager.set_state(user_id, "repairing")
    
    await query.edit_message_text(
        get_text(lang, "send_pdf_for_repair"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_ocr_start(query, user_id: int, lang: str) -> None:
    """Start OCR processing"""
    state_manager.set_state(user_id, "ocr_processing")
    
    await query.edit_message_text(
        get_text(lang, "send_pdf_for_ocr"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_images_to_pdf_start(query, user_id: int, lang: str) -> None:
    """Start collecting images for PDF"""
    state_manager.set_state(user_id, "collecting_images")
    state_manager.clear_files(user_id)
    
    await query.edit_message_text(
        get_text(lang, "send_images"),
        reply_markup=get_cancel_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_create_pdf_from_images(query, user_id: int, lang: str, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create PDF from collected images"""
    images = state_manager.get_files(user_id)
    
    if not images:
        await query.edit_message_text(
            get_text(lang, "no_images"),
            reply_markup=get_main_keyboard(user_id)
        )
        return
    
    await query.edit_message_text(
        get_text(lang, "creating_pdf", count=len(images))
    )
    
    try:
        output_path = await images_to_pdf(images)
        
        # Get file info
        from PyPDF2 import PdfReader
        reader = PdfReader(output_path)
        total_pages = len(reader.pages)
        file_size = get_file_size_mb(output_path)
        
        await context.bot.send_document(
            chat_id=user_id,
            document=open(output_path, 'rb'),
            filename="images.pdf",
            caption=get_text(lang, "pdf_created",
                           pages=total_pages,
                           size=f"{file_size:.2f}MB")
        )
        
        await context.bot.send_message(
            chat_id=user_id,
            text=get_text(lang, "success"),
            reply_markup=get_main_keyboard(user_id)
        )
        
        cleanup_files(images + [output_path])
        state_manager.clear_state(user_id)
        state_manager.clear_files(user_id)
        
    except Exception as e:
        logger.error(f"Images to PDF error: {e}", exc_info=True)
        await context.bot.send_message(
            chat_id=user_id,
            text=get_text(lang, "error"),
            reply_markup=get_main_keyboard(user_id)
        )


async def handle_word_to_pdf_start(query, user_id: int, lang: str) -> None:
    """Start Word to PDF conversion"""
    state_manager.set_state(user_id, "word_to_pdf")
    
    await query.edit_message_text(
        get_text(lang, "send_files"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_excel_to_pdf_start(query, user_id: int, lang: str) -> None:
    """Start Excel to PDF conversion"""
    state_manager.set_state(user_id, "excel_to_pdf")
    
    await query.edit_message_text(
        get_text(lang, "send_files"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_powerpoint_to_pdf_start(query, user_id: int, lang: str) -> None:
    """Start PowerPoint to PDF conversion"""
    state_manager.set_state(user_id, "powerpoint_to_pdf")
    
    await query.edit_message_text(
        get_text(lang, "send_files"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_pdf_to_jpg_start(query, user_id: int, lang: str) -> None:
    """Start PDF to JPG conversion"""
    state_manager.set_state(user_id, "pdf_to_jpg")
    
    await query.edit_message_text(
        get_text(lang, "send_one_pdf"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_pdf_to_word_start(query, user_id: int, lang: str) -> None:
    """Start PDF to Word conversion"""
    state_manager.set_state(user_id, "pdf_to_word")
    
    await query.edit_message_text(
        get_text(lang, "send_one_pdf"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_rotate_start(query, user_id: int, lang: str) -> None:
    """Start PDF rotation"""
    state_manager.set_state(user_id, "rotating")
    
    await query.edit_message_text(
        get_text(lang, "send_pdf_for_rotate"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_page_numbers_start(query, user_id: int, lang: str) -> None:
    """Start adding page numbers"""
    state_manager.set_state(user_id, "adding_page_numbers")
    
    await query.edit_message_text(
        get_text(lang, "send_one_pdf"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_watermark_start(query, user_id: int, lang: str) -> None:
    """Start adding watermark"""
    state_manager.set_state(user_id, "adding_watermark")
    
    await query.edit_message_text(
        get_text(lang, "send_pdf_for_watermark"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_unlock_start(query, user_id: int, lang: str) -> None:
    """Start unlocking PDF"""
    state_manager.set_state(user_id, "unlocking")
    
    await query.edit_message_text(
        get_text(lang, "send_pdf_for_unlock"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_protect_start(query, user_id: int, lang: str) -> None:
    """Start protecting PDF"""
    state_manager.set_state(user_id, "protecting")
    
    await query.edit_message_text(
        get_text(lang, "send_pdf_for_protect"),
        reply_markup=get_back_keyboard(user_id),
        parse_mode="Markdown"
    )


async def handle_coming_soon(query, user_id: int, lang: str, feature: str) -> None:
    """Handle coming soon features"""
    if is_subscribed(user_id):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔕 " + get_text(lang, "cancel"), callback_data="unsubscribe_coming")],
            [InlineKeyboardButton(get_text(lang, "back"), callback_data="back_to_menu")]
        ])
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔔 " + get_text(lang, "notify_me"), callback_data="subscribe_coming")],
            [InlineKeyboardButton(get_text(lang, "back"), callback_data="back_to_menu")]
        ])
    
    await query.edit_message_text(
        get_text(lang, "coming_soon"),
        reply_markup=keyboard
    )