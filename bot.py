#!/usr/bin/env python3
"""
Lexicon Track Adder Bot - Main bot implementation
"""

import os
import sys
import logging
import argparse
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import Config, load_config, save_config
from utils import is_admin, is_mp3_file, validate_directory
from download_manager import DownloadManager
from lexicon_client import LexiconClient, test_lexicon_connection
from error_handler import error_handler, handle_bot_error, ConfigurationError, DownloadError, LexiconError, PermissionError

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def setup_download_dir(download_dir):
    """Setup the download directory."""
    if validate_directory(download_dir):
        return download_dir
    else:
        print(f"❌ Invalid directory: {download_dir}")
        print("Please provide a valid path that exists and is writable.")
        print("Example: /Users/username/Music/Downloads")
        return None


def setup_lexicon_enabled(enabled):
    """Setup Lexicon integration choice."""
    if enabled.lower() in ['yes', 'y', 'true', '1']:
        return True
    elif enabled.lower() in ['no', 'n', 'false', '0']:
        return False
    else:
        print("Please specify 'yes' or 'no' for Lexicon integration.")
        return None


def setup_lexicon_url(lexicon_url):
    """Setup Lexicon URL configuration."""
    # Test connection
    print(f"Testing Lexicon API connection at {lexicon_url}...")
    
    if test_lexicon_connection(lexicon_url):
        return lexicon_url
    else:
        print(f"❌ Failed to connect to Lexicon API at {lexicon_url}")
        print("Please make sure Lexicon is running with the API enabled.")
        return None


def run_terminal_setup(args):
    """Run the terminal setup."""
    print("=== Lexicon Track Adder Bot Setup ===\n")
    
    # Load existing config or create new one
    config = load_config()
    
    # Setup download directory
    print("1. Download Directory Setup")
    download_dir = setup_download_dir(args.download_dir)
    if not download_dir:
        sys.exit(1)
    
    config.download_dir = download_dir
    print(f"✅ Download directory set to: {download_dir}\n")
    
    # Setup Lexicon integration
    print("2. Lexicon Integration Setup")
    lexicon_enabled = setup_lexicon_enabled(args.lexicon_enabled)
    if lexicon_enabled is None:
        sys.exit(1)
    
    config.lexicon_enabled = lexicon_enabled
    
    if lexicon_enabled:
        print("✅ Lexicon integration enabled.")
        
        # Setup Lexicon URL
        print("\n3. Lexicon API URL Setup")
        lexicon_url = setup_lexicon_url(args.lexicon_url)
        
        if lexicon_url:
            config.lexicon_api_url = lexicon_url
            print(f"✅ Lexicon API URL set to: {lexicon_url}")
        else:
            print("⚠️ Lexicon integration was enabled but URL setup failed. Disabling Lexicon integration.")
            config.lexicon_enabled = False
    else:
        print("✅ Lexicon integration disabled.")
    
    # Save config
    save_config(config)
    
    print("\n=== Setup Complete! ===")
    print("Your bot is now configured and ready to use.")
    print("You can start the bot by running: python bot.py")


@handle_bot_error
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    config = context.bot_data.get('config')
    
    if not config.is_configured():
        await update.message.reply_text(
            "Welcome to Lexicon Track Adder Bot!\n\n"
            "The bot is not configured yet. Please run the setup script first:\n\n"
            "`python bot.py --setup --download-dir /path/to/music --lexicon-enabled yes/no`\n\n"
            "Replace `/path/to/music` with your desired download directory.\n"
            "After setup is complete, restart the bot and send /start again."
        )
        return
    else:
        await update.message.reply_text(
            "Welcome back! Send me an MP3 file and I'll download it for you."
        )


@handle_bot_error
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    help_text = """
    *Lexicon Track Adder Bot Help*
    
    /start - Start the bot
    /help - Show this help message
    
    *Usage:*
    1. Get an MP3 file from @deezload2bot
    2. Forward that file to this bot
    3. The bot will download it to your specified folder
    4. If enabled, it will add the file to your Lexicon library
    
    *Setup:*
    If the bot is not configured, run:
    `python bot.py --setup --download-dir /path/to/music --lexicon-enabled yes/no`
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")


def main() -> None:
    """Start the bot or run setup."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Lexicon Track Adder Bot')
    parser.add_argument('--setup', action='store_true', help='Run setup instead of starting the bot')
    parser.add_argument('--download-dir', help='Directory to save music files (required for setup)')
    parser.add_argument('--lexicon-enabled', choices=['yes', 'no'], default='no', 
                        help='Enable Lexicon integration (yes/no)')
    parser.add_argument('--lexicon-url', default='http://localhost:48624/v1', 
                        help='Lexicon API URL (default: http://localhost:48624/v1)')
    
    args = parser.parse_args()
    
    # If setup flag is provided, run setup and exit
    if args.setup:
        if not args.download_dir:
            print("Error: --download-dir is required when using --setup")
            sys.exit(1)
        run_terminal_setup(args)
        return
    
    # Load configuration
    config = load_config()
    
    if not config.is_configured():
        print("Bot is not configured. Please run setup first:")
        print("python bot.py --setup --download-dir /path/to/music --lexicon-enabled yes/no")
        return
    
    if not config.bot_token:
        logger.error("No bot token provided. Set TELEGRAM_BOT_TOKEN environment variable or add to config.json")
        return
    
    # Create the Application
    application = Application.builder().token(config.bot_token).build()
    
    # Store config in bot_data for access in handlers
    application.bot_data['config'] = config
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Run the bot
    logger.info("Starting bot...")
    application.run_polling()


if __name__ == "__main__":
    main()
