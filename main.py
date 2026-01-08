#!/usr/bin/env python3
"""
PDF Bot - Main Entry Point
A comprehensive Telegram bot for PDF operations
"""

import logging
import logging.config
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config.settings import BOT_TOKEN, LOGGING_CONFIG
from bot import handlers, callbacks

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot"""
    
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found! Please set it in .env file")
        return
    
    logger.info("Starting PDF Bot...")
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", handlers.start_command))
    application.add_handler(CommandHandler("help", handlers.help_command))
    application.add_handler(CommandHandler("language", handlers.language_command))
    application.add_handler(CommandHandler("cancel", handlers.cancel_command))
    application.add_handler(CommandHandler("subscribe", handlers.subscribe_command))
    application.add_handler(CommandHandler("unsubscribe", handlers.unsubscribe_command))
    application.add_handler(CommandHandler("stats", handlers.stats_command))
    
    # Callback query handler for all buttons
    application.add_handler(CallbackQueryHandler(callbacks.button_callback))
    
    # Message handlers
    application.add_handler(
        MessageHandler(filters.Document.ALL, handlers.handle_document)
    )
    application.add_handler(
        MessageHandler(filters.PHOTO, handlers.handle_photo)
    )
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_text)
    )
    
    # Error handler
    application.add_error_handler(handlers.error_handler)
    
    # Start the bot
    logger.info("✅ PDF Bot started successfully!")
    logger.info("Bot is ready to accept messages...")
    
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)