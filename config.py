#!/usr/bin/env python3
"""
Configuration management for Lexicon Track Adder Bot
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class Config:
    """Configuration data class for the bot."""
    bot_token: str = ""
    admin_user_id: Optional[int] = None
    download_dir: str = ""
    lexicon_enabled: bool = False
    lexicon_api_url: str = "http://localhost:48624/v1"
    
    def is_configured(self) -> bool:
        """Check if the bot is properly configured."""
        return (
            bool(self.bot_token) and
            self.admin_user_id is not None and
            bool(self.download_dir)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create config from dictionary."""
        return cls(**data)


def load_config() -> Config:
    """Load configuration from file or create default."""
    config_file = "config.json"
    
    # Check if config file exists
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                return Config.from_dict(data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
            return Config()
    else:
        # Try to get bot token from environment variable
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        return Config(bot_token=bot_token)


def save_config(config: Config) -> bool:
    """Save configuration to file."""
    config_file = "config.json"
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config.to_dict(), f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving config: {e}")
        return False


def update_config(updates: Dict[str, Any]) -> bool:
    """Update existing configuration with new values."""
    config = load_config()
    
    # Update config with new values
    for key, value in updates.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    return save_config(config)
