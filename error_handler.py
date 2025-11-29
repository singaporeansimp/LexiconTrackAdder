#!/usr/bin/env python3
"""
Error handling for Lexicon Track Adder Bot
"""

import logging
import traceback
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def error_handler(update: Optional[Update], context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Log the error and send a telegram message to notify the user.
    
    Args:
        update: The update that caused the error
        context: The context of the error
    """
    # Log the error
    logger.error(f"Exception while handling an update: {context.error}")
    logger.error(traceback.format_exc())
    
    # Only send error message if we have a chat to send to
    if update and update.effective_chat:
        try:
            # Try to send a helpful error message
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ An error occurred while processing your request.\n"
                     "Please try again or contact the administrator if the problem persists."
            )
        except Exception as e:
            # If we can't even send the error message, just log it
            logger.error(f"Failed to send error message: {e}")


class BotError(Exception):
    """Base exception for bot-specific errors."""
    pass


class ConfigurationError(BotError):
    """Exception raised for configuration errors."""
    pass


class DownloadError(BotError):
    """Exception raised for download errors."""
    pass


class LexiconError(BotError):
    """Exception raised for Lexicon API errors."""
    pass


class PermissionError(BotError):
    """Exception raised for permission errors."""
    pass


def handle_bot_error(func):
    """Decorator to handle bot errors and provide user-friendly messages."""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ConfigurationError as e:
            # Handle configuration errors
            update = args[0] if args else None
            if update and hasattr(update, 'message'):
                await update.message.reply_text(
                    f"⚙️ Configuration error: {str(e)}\n"
                    "Please run /setup to reconfigure the bot."
                )
            logger.error(f"Configuration error: {e}")
        except DownloadError as e:
            # Handle download errors
            update = args[0] if args else None
            if update and hasattr(update, 'message'):
                await update.message.reply_text(
                    f"📥 Download error: {str(e)}\n"
                    "Please check your internet connection and try again."
                )
            logger.error(f"Download error: {e}")
        except LexiconError as e:
            # Handle Lexicon API errors
            update = args[0] if args else None
            if update and hasattr(update, 'message'):
                await update.message.reply_text(
                    f"🎵 Lexicon error: {str(e)}\n"
                    "The file was downloaded but not added to your library."
                )
            logger.error(f"Lexicon error: {e}")
        except PermissionError as e:
            # Handle permission errors
            update = args[0] if args else None
            if update and hasattr(update, 'message'):
                await update.message.reply_text(
                    f"🔒 Permission error: {str(e)}\n"
                    "This bot is private and only accessible to the administrator."
                )
            logger.error(f"Permission error: {e}")
        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            logger.error(traceback.format_exc())
            
            update = args[0] if args else None
            if update and hasattr(update, 'message'):
                await update.message.reply_text(
                    "❌ An unexpected error occurred.\n"
                    "Please try again or contact the administrator."
                )
    
    return wrapper
