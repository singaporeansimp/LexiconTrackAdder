#!/usr/bin/env python3
"""
Lexicon Track Adder Bot - Main bot implementation
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from config import Config, load_config, save_config
from setup import get_setup_conversation_handler, setup_conversation
from utils import is_admin, is_mp3_file
from download_manager import DownloadManager
from lexicon_client import LexiconClient
from error_handler import error_handler, handle_bot_error, ConfigurationError, DownloadError, LexiconError, PermissionError

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


@handle_bot_error
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the /start command."""
    config = context.bot_data.get('config')
    
    if not config.is_configured():
        await update.message.reply_text(
            "Welcome to Lexicon Track Adder Bot!\n\n"
            "Let's set up your bot. First, I need to know where you'd like to save your music files."
        )
        # Start setup conversation
        return await setup_conversation(update, context)
    else:
        await update.message.reply_text(
            "Welcome back! Send me an MP3 file and I'll download it for you."
        )
        return ConversationHandler.END


@handle_bot_error
async def setup_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the /setup command to reconfigure the bot."""
    await update.message.reply_text(
        "Let's reconfigure your bot settings.\n\n"
        "First, please provide the directory where you'd like to save your music files."
    )
    return await setup_conversation(update, context)


@handle_bot_error
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle document messages (MP3 files)."""
    config = context.bot_data.get('config')
    
    # Check if bot is configured
    if not config.is_configured():
        raise ConfigurationError("Bot is not configured yet. Please send /start to begin setup.")
    
    # Check if user is admin
    if not is_admin(update.effective_user.id, config):
        raise PermissionError("This bot is private and only accessible to the administrator.")
    
    # Check if file is MP3
    document = update.message.document
    if not is_mp3_file(document):
        await update.message.reply_text(
            "Please send only MP3 files."
        )
        return
    
    # Initialize download manager
    download_manager = DownloadManager(config.download_dir)
    
    # Download the file
    file_path = await download_manager.download_file(document, context, update)
    
    if not file_path:
        raise DownloadError("Failed to download the file.")
    
    if config.lexicon_enabled:
        # Add to Lexicon if enabled
        await update.message.reply_text("Adding to Lexicon library...")
        
        lexicon_client = LexiconClient(config.lexicon_api_url)
        track_data = lexicon_client.add_track(file_path)
        
        if track_data:
            title = track_data.get('title', 'Unknown')
            artist = track_data.get('artist', 'Unknown')
            await update.message.reply_text(
                f"✅ Added to Lexicon library:\n"
                f"Title: {title}\n"
                f"Artist: {artist}"
            )
        else:
            raise LexiconError("Failed to add track to Lexicon library.")


@handle_bot_error
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    help_text = """
    *Lexicon Track Adder Bot Help*
    
    /start - Start the bot or begin setup
    /setup - Reconfigure the bot settings
    /help - Show this help message
    
    *Usage:*
    1. Get an MP3 file from @deezload2bot
    2. Forward that file to this bot
    3. The bot will download it to your specified folder
    4. If enabled, it will add the file to your Lexicon library
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")


def main() -> None:
    """Start the bot."""
    # Load or create configuration
    config = load_config()
    
    if not config.bot_token:
        logger.error("No bot token provided. Set TELEGRAM_BOT_TOKEN environment variable or add to config.json")
        return
    
    # Create the Application
    application = Application.builder().token(config.bot_token).build()
    
    # Store config in bot_data for access in handlers
    application.bot_data['config'] = config
    
    # Get setup conversation handler
    setup_handler = get_setup_conversation_handler()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setup", setup_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(setup_handler)
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Run the bot
    logger.info("Starting bot...")
    application.run_polling()


if __name__ == "__main__":
    main()
