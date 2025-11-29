#!/usr/bin/env python3
"""
Download manager for handling file downloads from Telegram
"""

import os
import asyncio
import logging
from typing import Optional, Callable
from telegram import Update, Document
from telegram.ext import ContextTypes
from utils import sanitize_filename, format_file_size
from error_handler import handle_bot_error, DownloadError

logger = logging.getLogger(__name__)


class DownloadManager:
    """Manages file downloads from Telegram."""
    
    def __init__(self, download_dir: str):
        self.download_dir = download_dir
        self.active_downloads = {}  # Track active downloads by message_id
    
    @handle_bot_error
    async def download_file(
        self, 
        document, 
        context: ContextTypes.DEFAULT_TYPE,
        update: Update,
        progress_callback: Optional[Callable] = None
    ) -> Optional[str]:
        """
        Download a file from Telegram.
        
        Args:
            document: The Telegram document or audio object
            context: The Telegram context
            update: The Telegram update
            progress_callback: Optional callback for progress updates
            
        Returns:
            Path to the downloaded file, or None if failed
        """
        file_name = getattr(document, 'file_name', None) or f"{getattr(document, 'title', 'audio')}.mp3"
        file_id = document.file_id
        file_size = getattr(document, 'file_size', 0)
        
        # Validate inputs
        if not file_name or not file_id:
            raise DownloadError("Invalid file information provided.")
        
        # Sanitize filename
        safe_filename = sanitize_filename(file_name)
        file_path = os.path.join(self.download_dir, safe_filename)
        
        # Handle duplicate filenames
        counter = 1
        original_path = file_path
        while os.path.exists(file_path):
            name, ext = os.path.splitext(original_path)
            file_path = f"{name}_{counter}{ext}"
            counter += 1
        
        try:
            # Get file object from Telegram
            file = await context.bot.get_file(file_id)
            
            # Send initial message
            await update.message.reply_text(
                f"📥 Starting download: {safe_filename}\n"
                f"Size: {format_file_size(file_size)}"
            )
            
            # Download the file
            await file.download_to_drive(file_path)
            
            # Verify file was downloaded
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                await update.message.reply_text(
                    f"✅ Download complete: {safe_filename}\n"
                    f"Saved to: {file_path}"
                )
                return file_path
            else:
                raise DownloadError("File was not saved correctly.")
                
        except Exception as e:
            # Clean up partial download if it exists
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError:
                    logger.error(f"Failed to remove partial download: {file_path}")
            
            # Re-raise as DownloadError
            if isinstance(e, DownloadError):
                raise
            else:
                raise DownloadError(f"Failed to download file: {str(e)}")
    
    def get_download_info(self, file_path: str) -> dict:
        """Get information about a downloaded file."""
        if not os.path.exists(file_path):
            return {}
        
        try:
            stat = os.stat(file_path)
            return {
                "path": file_path,
                "name": os.path.basename(file_path),
                "size": stat.st_size,
                "size_formatted": format_file_size(stat.st_size),
                "modified": stat.st_mtime
            }
        except OSError as e:
            logger.error(f"Error getting file info for {file_path}: {e}")
            return {}
