#!/usr/bin/env python3
"""
Utility functions for Lexicon Track Adder Bot
"""

import os
from typing import Optional
from telegram import Document


def is_admin(user_id: int, config) -> bool:
    """Check if user is the administrator."""
    return user_id == config.admin_user_id


def is_mp3_file(document: Document) -> bool:
    """Check if document is an MP3 file."""
    if not document:
        return False
    
    # Check file name extension
    if document.file_name and document.file_name.lower().endswith('.mp3'):
        return True
    
    # Check mime type
    if document.mime_type and document.mime_type == 'audio/mpeg':
        return True
    
    return False


def validate_directory(path: str) -> bool:
    """Validate if directory exists and is writable."""
    if not path:
        return False
    
    # Check if directory exists
    if not os.path.exists(path):
        try:
            # Try to create directory
            os.makedirs(path, exist_ok=True)
        except OSError:
            return False
    
    # Check if path is a directory
    if not os.path.isdir(path):
        return False
    
    # Check if directory is writable
    return os.access(path, os.W_OK)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system usage."""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "unnamed_file"
    
    return filename
