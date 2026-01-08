"""
Message and Command Handlers
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from config.texts import get_text
from config.settings import ADMIN_IDS, MAX_FILE_SIZE_MB
from bot.keyboards import (
    get_main_keyboard,
    get_language_keyboard,
    get_back_keyboard
)
from bot.states import UserStateManager, get_user_language
from utils.file_manager import download_file, cleanup_files, get_file_size_mb
from utils.subscriber_manager import add_subscriber, remove_subscriber, is_subscribed
from services.pdf_converter import convert_image_to_pdf, convert_document_to_pdf
from services.pdf_organizer import merge_pdfs, extract_pages, remove_pages
from services.pdf_optimizer import compress_pdf, repair_pdf
from services.pdf_editor import rotate_pdf, add_watermark, add_page_numbers
from services.pdf_security import unlock_pdf, protect_pdf
from services.image_processor import images_to_pdf

logger = logging.getLogger(__name__)
state_manager = UserStateManager()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    logger.info(f"User {user_id} ({user_name}) started the bot")
    
    welcome_text = get_text(get_user_language(user_id), "welcome")
    
    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_language_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    help_text = get_text(lang, "help")
    
    await update.message.reply_text(
        help_text,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(user_id)
    )


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /language command"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    text = get_text(lang, "choose_language")
    
    await update.message.reply_text(
        text,
        reply_markup=get_language_keyboard()
    )


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /cancel command"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    # Clear user state
    state_manager.clear_state(user_id)
    state_manager.clear_files(user_id)
    
    text = get_text(lang, "operation_cancelled")
    
    await update.message.reply_text(
        text,
        reply_markup=get_main_keyboard(user_id)
    )


async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /subscribe command"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if is_subscribed(user_id):
        text = get_text(lang, "already_subscribed")
    else:
        add_subscriber(user_id)
        text = get_text(lang, "subscribed")
    
    await update.message.reply_text(text)


async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /unsubscribe command"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if not is_subscribed(user_id):
        text = get_text(lang, "not_subscribed")
    else:
        remove_subscriber(user_id)
        text = get_text(lang, "unsubscribed")
    
    await update.message.reply_text(text)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command (admin only)"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Admin only command")
        return
    
    # TODO: Implement statistics
    stats_text = "📊 *Bot Statistics:*\n\n" \
                 "Total users: Coming soon\n" \
                 "Active today: Coming soon\n" \
                 "PDFs processed: Coming soon"
    
    await update.message.reply_text(stats_text, parse_mode="Markdown")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle document uploads"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    document = update.message.document
    
    # Check file size
    file_size_mb = document.file_size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        await update.message.reply_text(
            get_text(lang, "file_too_large", max_size=MAX_FILE_SIZE_MB)
        )
        return
    
    state = state_manager.get_state(user_id)
    logger.info(f"User {user_id} uploaded document in state: {state}")
    
    try:
        # Download file
        file_path = await download_file(
            context.bot,
            document.file_id,
            document.file_name
        )
        
        # Handle based on state
        if state == "merging":
            await handle_merge_document(update, context, file_path)
            
        elif state == "compressing":
            await handle_compress_document(update, context, file_path)
            
        elif state == "rotating":
            await handle_rotate_document(update, context, file_path)
            
        elif state == "unlocking":
            await handle_unlock_document(update, context, file_path)
            
        elif state == "protecting":
            await handle_protect_document(update, context, file_path)
            
        elif state == "extracting_pages":
            await handle_extract_pages_document(update, context, file_path)
            
        elif state == "removing_pages":
            await handle_remove_pages_document(update, context, file_path)
            
        elif state == "adding_watermark":
            await handle_watermark_document(update, context, file_path)
            
        elif state == "adding_page_numbers":
            await handle_page_numbers_document(update, context, file_path)
            
        else:
            # Default: convert to PDF
            await handle_convert_document(update, context, file_path)
            
    except Exception as e:
        logger.error(f"Error handling document: {e}", exc_info=True)
        await update.message.reply_text(get_text(lang, "error"))


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photo uploads"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    photo = update.message.photo[-1]  # Get largest photo
    
    state = state_manager.get_state(user_id)
    logger.info(f"User {user_id} uploaded photo in state: {state}")
    
    try:
        # Download photo
        file_path = await download_file(
            context.bot,
            photo.file_id,
            f"image_{user_id}_{len(state_manager.get_files(user_id))}.jpg"
        )
        
        if state == "collecting_images":
            # Add to image collection
            state_manager.add_file(user_id, file_path)
            count = len(state_manager.get_files(user_id))
            
            from bot.keyboards import get_done_keyboard
            await update.message.reply_text(
                get_text(lang, "images_count", count=count),
                reply_markup=get_done_keyboard(user_id),
                parse_mode="Markdown"
            )
            
        elif state == "adding_watermark" and state_manager.get_temp(user_id, "pdf_path"):
            # This is the watermark image
            await handle_watermark_image(update, context, file_path)
            
        else:
            # Default: convert single image to PDF
            await handle_convert_image(update, context, file_path)
            
    except Exception as e:
        logger.error(f"Error handling photo: {e}", exc_info=True)
        await update.message.reply_text(get_text(lang, "error"))


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    text = update.message.text
    
    state = state_manager.get_state(user_id)
    logger.info(f"User {user_id} sent text in state: {state}")
    
    try:
        if state == "rotating_wait_angle":
            await handle_rotation_angle(update, context, text)
            
        elif state == "unlocking_wait_password":
            await handle_unlock_password(update, context, text)
            
        elif state == "protecting_wait_password":
            await handle_protect_password(update, context, text)
            
        elif state == "extracting_pages_wait_spec":
            await handle_extract_pages_spec(update, context, text)
            
        elif state == "removing_pages_wait_spec":
            await handle_remove_pages_spec(update, context, text)
            
        elif state == "compressing_wait_level":
            await handle_compression_level(update, context, text)
            
        else:
            # Unknown state or no operation pending
            await update.message.reply_text(
                get_text(lang, "choose_action"),
                reply_markup=get_main_keyboard(user_id)
            )
            
    except Exception as e:
        logger.error(f"Error handling text: {e}", exc_info=True)
        await update.message.reply_text(get_text(lang, "error"))


# Helper functions for specific operations

async def handle_merge_document(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str) -> None:
    """Handle document for merging"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if not file_path.lower().endswith('.pdf'):
        await update.message.reply_text("❌ Please send PDF files only")
        cleanup_files([file_path])
        return
    
    state_manager.add_file(user_id, file_path)
    count = len(state_manager.get_files(user_id))
    
    from bot.keyboards import get_merge_keyboard
    await update.message.reply_text(
        get_text(lang, "pdfs_count", count=count),
        reply_markup=get_merge_keyboard(user_id, count),
        parse_mode="Markdown"
    )


async def handle_compress_document(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str) -> None:
    """Handle document for compression"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if not file_path.lower().endswith('.pdf'):
        await update.message.reply_text("❌ Please send a PDF file")
        cleanup_files([file_path])
        return
    
    # Ask for compression level
    state_manager.set_temp(user_id, "pdf_path", file_path)
    state_manager.set_state(user_id, "compressing_wait_level")
    
    await update.message.reply_text(
        get_text(lang, "enter_compression_level"),
        parse_mode="Markdown"
    )


async def handle_rotate_document(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str) -> None:
    """Handle document for rotation"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if not file_path.lower().endswith('.pdf'):
        await update.message.reply_text("❌ Please send a PDF file")
        cleanup_files([file_path])
        return
    
    state_manager.set_temp(user_id, "pdf_path", file_path)
    state_manager.set_state(user_id, "rotating_wait_angle")
    
    await update.message.reply_text(get_text(lang, "enter_rotation"))


async def handle_unlock_document(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str) -> None:
    """Handle document for unlocking"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if not file_path.lower().endswith('.pdf'):
        await update.message.reply_text("❌ Please send a PDF file")
        cleanup_files([file_path])
        return
    
    state_manager.set_temp(user_id, "pdf_path", file_path)
    state_manager.set_state(user_id, "unlocking_wait_password")
    
    await update.message.reply_text(get_text(lang, "enter_password"))


async def handle_protect_document(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str) -> None:
    """Handle document for protection"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if not file_path.lower().endswith('.pdf'):
        await update.message.reply_text("❌ Please send a PDF file")
        cleanup_files([file_path])
        return
    
    state_manager.set_temp(user_id, "pdf_path", file_path)
    state_manager.set_state(user_id, "protecting_wait_password")
    
    await update.message.reply_text(get_text(lang, "enter_new_password"))


async def handle_extract_pages_document(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str) -> None:
    """Handle document for page extraction"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if not file_path.lower().endswith('.pdf'):
        await update.message.reply_text("❌ Please send a PDF file")
        cleanup_files([file_path])
        return
    
    state_manager.set_temp(user_id, "pdf_path", file_path)
    state_manager.set_state(user_id, "extracting_pages_wait_spec")
    
    await update.message.reply_text(
        get_text(lang, "enter_pages"),
        parse_mode="Markdown"
    )


async def handle_remove_pages_document(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str) -> None:
    """Handle document for page removal"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if not file_path.lower().endswith('.pdf'):
        await update.message.reply_text("❌ Please send a PDF file")
        cleanup_files([file_path])
        return
    
    state_manager.set_temp(user_id, "pdf_path", file_path)
    state_manager.set_state(user_id, "removing_pages_wait_spec")
    
    await update.message.reply_text(
        get_text(lang, "enter_pages"),
        parse_mode="Markdown"
    )


async def handle_watermark_document(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str) -> None:
    """Handle document for watermark"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if not file_path.lower().endswith('.pdf'):
        await update.message.reply_text("❌ Please send a PDF file")
        cleanup_files([file_path])
        return
    
    state_manager.set_temp(user_id, "pdf_path", file_path)
    
    await update.message.reply_text(get_text(lang, "send_watermark_image"))


async def handle_watermark_image(update: Update, context: ContextTypes.DEFAULT_TYPE, image_path: str) -> None:
    """Handle watermark image"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    pdf_path = state_manager.get_temp(user_id, "pdf_path")
    
    await update.message.reply_text(get_text(lang, "adding_watermark"))
    
    try:
        output_path = await add_watermark(pdf_path, image_path)
        
        await update.message.reply_document(
            document=open(output_path, 'rb'),
            filename="watermarked.pdf"
        )
        
        await update.message.reply_text(
            get_text(lang, "watermark_added"),
            reply_markup=get_main_keyboard(user_id)
        )
        
        cleanup_files([pdf_path, image_path, output_path])
        state_manager.clear_state(user_id)
        
    except Exception as e:
        logger.error(f"Watermark error: {e}", exc_info=True)
        await update.message.reply_text(get_text(lang, "error"))
        cleanup_files([pdf_path, image_path])


async def handle_page_numbers_document(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str) -> None:
    """Handle document for page numbers"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if not file_path.lower().endswith('.pdf'):
        await update.message.reply_text("❌ Please send a PDF file")
        cleanup_files([file_path])
        return
    
    await update.message.reply_text(get_text(lang, "adding_page_numbers"))
    
    try:
        output_path = await add_page_numbers(file_path)
        
        await update.message.reply_document(
            document=open(output_path, 'rb'),
            filename="numbered.pdf"
        )
        
        await update.message.reply_text(
            get_text(lang, "page_numbers_added"),
            reply_markup=get_main_keyboard(user_id)
        )
        
        cleanup_files([file_path, output_path])
        state_manager.clear_state(user_id)
        
    except Exception as e:
        logger.error(f"Page numbers error: {e}", exc_info=True)
        await update.message.reply_text(get_text(lang, "error"))
        cleanup_files([file_path])


async def handle_convert_document(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str) -> None:
    """Handle document conversion to PDF"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    await update.message.reply_text(get_text(lang, "converting"))
    
    try:
        output_path = await convert_document_to_pdf(file_path)
        
        await update.message.reply_document(
            document=open(output_path, 'rb'),
            filename="converted.pdf"
        )
        
        await update.message.reply_text(
            get_text(lang, "success"),
            reply_markup=get_main_keyboard(user_id)
        )
        
        cleanup_files([file_path, output_path])
        
    except Exception as e:
        logger.error(f"Conversion error: {e}", exc_info=True)
        await update.message.reply_text(get_text(lang, "error"))
        cleanup_files([file_path])


async def handle_convert_image(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str) -> None:
    """Handle single image conversion to PDF"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    await update.message.reply_text(get_text(lang, "converting"))
    
    try:
        output_path = await convert_image_to_pdf(file_path)
        
        await update.message.reply_document(
            document=open(output_path, 'rb'),
            filename="image.pdf"
        )
        
        await update.message.reply_text(
            get_text(lang, "success"),
            reply_markup=get_main_keyboard(user_id)
        )
        
        cleanup_files([file_path, output_path])
        
    except Exception as e:
        logger.error(f"Image conversion error: {e}", exc_info=True)
        await update.message.reply_text(get_text(lang, "error"))
        cleanup_files([file_path])


# Text input handlers

async def handle_rotation_angle(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    """Handle rotation angle input"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    try:
        angle = int(text.strip())
        if angle not in [90, 180, 270]:
            await update.message.reply_text(get_text(lang, "invalid_rotation"))
            return
        
        pdf_path = state_manager.get_temp(user_id, "pdf_path")
        await update.message.reply_text(get_text(lang, "rotating_pdf"))
        
        output_path = await rotate_pdf(pdf_path, angle)
        
        await update.message.reply_document(
            document=open(output_path, 'rb'),
            filename="rotated.pdf"
        )
        
        await update.message.reply_text(
            get_text(lang, "pdf_rotated", angle=angle),
            reply_markup=get_main_keyboard(user_id)
        )
        
        cleanup_files([pdf_path, output_path])
        state_manager.clear_state(user_id)
        
    except ValueError:
        await update.message.reply_text(get_text(lang, "invalid_rotation"))
    except Exception as e:
        logger.error(f"Rotation error: {e}", exc_info=True)
        await update.message.reply_text(get_text(lang, "error"))


async def handle_unlock_password(update: Update, context: ContextTypes.DEFAULT_TYPE, password: str) -> None:
    """Handle password for unlocking"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    try:
        pdf_path = state_manager.get_temp(user_id, "pdf_path")
        await update.message.reply_text(get_text(lang, "unlocking_pdf"))
        
        output_path = await unlock_pdf(pdf_path, password)
        
        await update.message.reply_document(
            document=open(output_path, 'rb'),
            filename="unlocked.pdf"
        )
        
        await update.message.reply_text(
            get_text(lang, "pdf_unlocked"),
            reply_markup=get_main_keyboard(user_id)
        )
        
        cleanup_files([pdf_path, output_path])
        state_manager.clear_state(user_id)
        
    except Exception as e:
        logger.error(f"Unlock error: {e}", exc_info=True)
        await update.message.reply_text(
            get_text(lang, "password_incorrect")
        )


async def handle_protect_password(update: Update, context: ContextTypes.DEFAULT_TYPE, password: str) -> None:
    """Handle password for protection"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    try:
        pdf_path = state_manager.get_temp(user_id, "pdf_path")
        await update.message.reply_text(get_text(lang, "protecting_pdf"))
        
        output_path = await protect_pdf(pdf_path, password)
        
        await update.message.reply_document(
            document=open(output_path, 'rb'),
            filename="protected.pdf"
        )
        
        await update.message.reply_text(
            get_text(lang, "pdf_protected"),
            reply_markup=get_main_keyboard(user_id)
        )
        
        cleanup_files([pdf_path, output_path])
        state_manager.clear_state(user_id)
        
    except Exception as e:
        logger.error(f"Protection error: {e}", exc_info=True)
        await update.message.reply_text(get_text(lang, "error"))


async def handle_extract_pages_spec(update: Update, context: ContextTypes.DEFAULT_TYPE, page_spec: str) -> None:
    """Handle page specification for extraction"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    try:
        pdf_path = state_manager.get_temp(user_id, "pdf_path")
        await update.message.reply_text(get_text(lang, "extracting_pages"))
        
        output_path = await extract_pages(pdf_path, page_spec)
        
        await update.message.reply_document(
            document=open(output_path, 'rb'),
            filename="extracted.pdf"
        )
        
        await update.message.reply_text(
            get_text(lang, "success"),
            reply_markup=get_main_keyboard(user_id)
        )
        
        cleanup_files([pdf_path, output_path])
        state_manager.clear_state(user_id)
        
    except Exception as e:
        logger.error(f"Extract pages error: {e}", exc_info=True)
        await update.message.reply_text(get_text(lang, "invalid_pages"))


async def handle_remove_pages_spec(update: Update, context: ContextTypes.DEFAULT_TYPE, page_spec: str) -> None:
    """Handle page specification for removal"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    try:
        pdf_path = state_manager.get_temp(user_id, "pdf_path")
        await update.message.reply_text(get_text(lang, "removing_pages"))
        
        output_path = await remove_pages(pdf_path, page_spec)
        
        await update.message.reply_document(
            document=open(output_path, 'rb'),
            filename="removed.pdf"
        )
        
        await update.message.reply_text(
            get_text(lang, "success"),
            reply_markup=get_main_keyboard(user_id)
        )
        
        cleanup_files([pdf_path, output_path])
        state_manager.clear_state(user_id)
        
    except Exception as e:
        logger.error(f"Remove pages error: {e}", exc_info=True)
        await update.message.reply_text(get_text(lang, "invalid_pages"))


async def handle_compression_level(update: Update, context: ContextTypes.DEFAULT_TYPE, level: str) -> None:
    """Handle compression level input"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    try:
        level_num = int(level.strip())
        if level_num not in [1, 2, 3]:
            await update.message.reply_text("❌ Please enter 1, 2, or 3")
            return
        
        quality = ["low", "medium", "high"][level_num - 1]
        
        pdf_path = state_manager.get_temp(user_id, "pdf_path")
        original_size = get_file_size_mb(pdf_path)
        
        await update.message.reply_text(get_text(lang, "compressing_pdf"))
        
        output_path = await compress_pdf(pdf_path, quality)
        compressed_size = get_file_size_mb(output_path)
        saved_percent = int((1 - compressed_size / original_size) * 100) if original_size > 0 else 0
        
        await update.message.reply_document(
            document=open(output_path, 'rb'),
            filename="compressed.pdf"
        )
        
        await update.message.reply_text(
            get_text(lang, "pdf_compressed",
                    original=f"{original_size:.2f}MB",
                    compressed=f"{compressed_size:.2f}MB",
                    saved=saved_percent),
            reply_markup=get_main_keyboard(user_id)
        )
        
        cleanup_files([pdf_path, output_path])
        state_manager.clear_state(user_id)
        
    except ValueError:
        await update.message.reply_text("❌ Please enter 1, 2, or 3")
    except Exception as e:
        logger.error(f"Compression error: {e}", exc_info=True)
        await update.message.reply_text(get_text(lang, "error"))


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)