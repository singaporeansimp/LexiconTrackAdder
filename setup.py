#!/usr/bin/env python3
"""
Setup conversation flow for first-time users
"""

import os
from typing import Dict, Any
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config import Config, save_config
from utils import validate_directory
from lexicon_client import test_lexicon_connection
from error_handler import handle_bot_error, ConfigurationError

# Conversation states
SETUP_DOWNLOAD_DIR = 1
SETUP_LEXICON_ENABLED = 2
SETUP_LEXICON_URL = 3
SETUP_COMPLETE = 4


@handle_bot_error
async def setup_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the setup conversation."""
    config = context.bot_data.get('config')
    
    # Set admin user ID if not already set
    if config.admin_user_id is None:
        config.admin_user_id = update.effective_user.id
        save_config(config)
        context.bot_data['config'] = config
    
    await update.message.reply_text(
        "Let's configure your bot!\n\n"
        "First, please provide the directory where you'd like to save your music files.\n"
        "This directory must exist and be writable.\n\n"
        "Example: /Users/username/Music/Downloads"
    )
    
    return SETUP_DOWNLOAD_DIR


@handle_bot_error
async def setup_download_dir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle download directory input."""
    download_dir = update.message.text.strip()
    
    # Validate directory
    if not validate_directory(download_dir):
        await update.message.reply_text(
            "❌ Invalid directory. Please provide a valid path that exists and is writable.\n"
            "Example: /Users/username/Music/Downloads"
        )
        return SETUP_DOWNLOAD_DIR
    
    # Update config
    config = context.bot_data.get('config')
    config.download_dir = download_dir
    save_config(config)
    context.bot_data['config'] = config
    
    await update.message.reply_text(
        f"✅ Download directory set to: {download_dir}\n\n"
        "Next, would you like to enable Lexicon integration?\n"
        "This will automatically add downloaded tracks to your Lexicon library.\n\n"
        "Reply with 'yes' or 'no'"
    )
    
    return SETUP_LEXICON_ENABLED


@handle_bot_error
async def setup_lexicon_enabled(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Lexicon integration choice."""
    response = update.message.text.strip().lower()
    
    if response in ['yes', 'y', 'true', '1']:
        config = context.bot_data.get('config')
        config.lexicon_enabled = True
        save_config(config)
        context.bot_data['config'] = config
        
        await update.message.reply_text(
            "✅ Lexicon integration enabled.\n\n"
            "By default, I'll use the standard Lexicon API URL: http://localhost:48624/v1\n"
            "Would you like to use a different URL?\n\n"
            "Reply with the new URL or 'no' to use the default"
        )
        
        return SETUP_LEXICON_URL
    elif response in ['no', 'n', 'false', '0']:
        config = context.bot_data.get('config')
        config.lexicon_enabled = False
        save_config(config)
        context.bot_data['config'] = config
        
        await update.message.reply_text(
            "✅ Lexicon integration disabled.\n\n"
            "Setup complete! 🎉\n\n"
            "You can now send me MP3 files and I'll download them to your specified directory.\n"
            "If you want to enable Lexicon integration later, just send /setup again."
        )
        
        return SETUP_COMPLETE
    else:
        await update.message.reply_text(
            "Please reply with 'yes' or 'no'."
        )
        return SETUP_LEXICON_ENABLED


@handle_bot_error
async def setup_lexicon_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Lexicon URL configuration."""
    response = update.message.text.strip()
    
    if response.lower() in ['no', 'n', 'default']:
        # Use default URL
        lexicon_url = "http://localhost:48624/v1"
    else:
        # Use provided URL
        lexicon_url = response
    
    # Test connection
    await update.message.reply_text("Testing Lexicon API connection...")
    
    if test_lexicon_connection(lexicon_url):
        config = context.bot_data.get('config')
        config.lexicon_api_url = lexicon_url
        save_config(config)
        context.bot_data['config'] = config
        
        await update.message.reply_text(
            f"✅ Lexicon API connection successful!\n\n"
            f"URL: {lexicon_url}\n\n"
            "Setup complete! 🎉\n\n"
            "You can now send me MP3 files and I'll download them to your specified directory "
            "and add them to your Lexicon library."
        )
    else:
        await update.message.reply_text(
            f"❌ Failed to connect to Lexicon API at {lexicon_url}\n\n"
            "Please make sure Lexicon is running with the API enabled.\n"
            "You can try again with /setup or continue without Lexicon integration."
        )
    
    return SETUP_COMPLETE


async def setup_complete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End the setup conversation."""
    return ConversationHandler.END


def get_setup_conversation_handler() -> ConversationHandler:
    """Create and return the setup conversation handler."""
    return ConversationHandler(
        entry_points=[],
        states={
            SETUP_DOWNLOAD_DIR: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, setup_download_dir)
            ],
            SETUP_LEXICON_ENABLED: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, setup_lexicon_enabled)
            ],
            SETUP_LEXICON_URL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, setup_lexicon_url)
            ],
            SETUP_COMPLETE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, setup_complete)
            ],
        },
        fallbacks=[],
    )
