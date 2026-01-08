#!/usr/bin/env python3
"""
PDF Bot - Main Entry Point
A comprehensive Telegram bot for PDF operations
"""

import logging
import logging.config
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
import asyncio
import threading
import time

from config.settings import (
    BOT_TOKEN, LOGGING_CONFIG, USE_WEBHOOK, WEBHOOK_URL,
    WEBHOOK_PATH, PORT
)
from bot import handlers, callbacks

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Global variables
application = None
flask_app = Flask(__name__)
loop = None


def create_application():
    """Create and configure the bot application"""
    global application

    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found! Please set it in .env file")
        return None

    logger.info("Creating PDF Bot application...")

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

    return application


@flask_app.route('/')
def health_check():
    """Health check endpoint for Render"""
    return {"status": "ok", "message": "PDF Bot is running"}


@flask_app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    """Webhook endpoint for Telegram updates"""
    global loop

    if not application or not loop:
        return {"error": "Bot not initialized"}, 500

    try:
        # Get the update from Telegram
        update_data = request.get_json()
        if not update_data:
            return {"error": "No JSON data received"}, 400

        # Create Update object
        update = Update.de_json(update_data, application.bot)

        # Process the update asynchronously
        asyncio.run_coroutine_threadsafe(process_update(update), loop)

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"error": str(e)}, 500


async def process_update(update: Update):
    """Process a Telegram update asynchronously"""
    try:
        await application.process_update(update)
    except Exception as e:
        logger.error(f"Error processing update: {e}")


def run_flask():
    """Run the Flask web server"""
    try:
        logger.info(f"Starting Flask server on port {PORT}")
        flask_app.run(host='0.0.0.0', port=PORT, debug=False)
    except Exception as e:
        logger.error(f"Flask server error: {e}")


async def run_webhook():
    """Run the bot with webhook"""
    global application, loop

    if not WEBHOOK_URL:
        logger.error("WEBHOOK_URL not set! Please set it in environment variables")
        return

    app = create_application()
    if not app:
        return

    # Initialize the application
    await app.initialize()
    application = app  # Set the global application
    loop = asyncio.get_event_loop()  # Set the global loop

    # Set webhook
    webhook_full_url = f"{WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"
    logger.info(f"Setting webhook to: {webhook_full_url}")

    try:
        await app.bot.set_webhook(url=webhook_full_url)
        logger.info("✅ Webhook set successfully!")

        # Start Flask server in a separate thread
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # Keep the main thread alive
        while True:
            await asyncio.sleep(60)  # Check every minute
            logger.info("Bot is running with webhook...")

    except Exception as e:
        logger.error(f"Webhook setup error: {e}")
    finally:
        if app:
            await app.bot.delete_webhook()


async def run_polling():
    """Run the bot with polling (for local development)"""
    app = create_application()
    if not app:
        return

    logger.info("✅ PDF Bot started successfully with polling!")
    logger.info("Bot is ready to accept messages...")

    try:
        await app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
    except Exception as e:
        logger.error(f"Polling error: {e}")


def main() -> None:
    """Start the bot"""
    logger.info("Starting PDF Bot...")

    if USE_WEBHOOK:
        logger.info("Using webhook mode (for production)")
        asyncio.run(run_webhook())
    else:
        logger.info("Using polling mode (for local development)")
        asyncio.run(run_polling())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)