#!/usr/bin/env python3
"""
Test script for Lexicon Track Adder Bot
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch, AsyncMock

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config, load_config, save_config
from utils import is_admin, is_mp3_file, validate_directory, sanitize_filename
from lexicon_client import LexiconClient
from download_manager import DownloadManager


class TestConfig(unittest.TestCase):
    """Test configuration management."""
    
    def test_config_creation(self):
        """Test creating a new config."""
        config = Config()
        self.assertEqual(config.bot_token, "")
        self.assertIsNone(config.admin_user_id)
        self.assertEqual(config.download_dir, "")
        self.assertFalse(config.lexicon_enabled)
        self.assertEqual(config.lexicon_api_url, "http://localhost:48624/v1")
    
    def test_config_is_configured(self):
        """Test configuration status check."""
        config = Config()
        self.assertFalse(config.is_configured())
        
        config.bot_token = "test_token"
        config.download_dir = "/test/dir"
        self.assertTrue(config.is_configured())
    
    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = Config(bot_token="test", admin_user_id=123)
        config_dict = config.to_dict()
        self.assertEqual(config_dict["bot_token"], "test")
        self.assertEqual(config_dict["admin_user_id"], 123)
    
    def test_config_from_dict(self):
        """Test creating config from dictionary."""
        data = {"bot_token": "test", "admin_user_id": 123}
        config = Config.from_dict(data)
        self.assertEqual(config.bot_token, "test")
        self.assertEqual(config.admin_user_id, 123)


class TestUtils(unittest.TestCase):
    """Test utility functions."""
    
    def test_is_admin(self):
        """Test admin check."""
        config = Config(admin_user_id=12345)
        self.assertTrue(is_admin(12345, config))
        self.assertFalse(is_admin(54321, config))
    
    def test_is_mp3_file(self):
        """Test MP3 file validation."""
        # Mock document with MP3 file
        doc_mp3 = Mock()
        doc_mp3.file_name = "test.mp3"
        doc_mp3.mime_type = "audio/mpeg"
        self.assertTrue(is_mp3_file(doc_mp3))
        
        # Mock document with non-MP3 file
        doc_other = Mock()
        doc_other.file_name = "test.txt"
        doc_other.mime_type = "text/plain"
        self.assertFalse(is_mp3_file(doc_other))
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Test with invalid characters
        self.assertEqual(sanitize_filename("test<>file.mp3"), "test__file.mp3")
        
        # Test with leading/trailing spaces and dots
        self.assertEqual(sanitize_filename("  .test.mp3.  "), "test.mp3")
        
        # Test with empty string
        self.assertEqual(sanitize_filename(""), "unnamed_file")


class TestLexiconClient(unittest.TestCase):
    """Test Lexicon API client."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = LexiconClient("http://test.example.com/v1")
    
    @patch('requests.Session.get')
    def test_test_connection_success(self, mock_get):
        """Test successful connection test."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = self.client.test_connection()
        self.assertTrue(result)
    
    @patch('requests.Session.get')
    def test_test_connection_failure(self, mock_get):
        """Test failed connection test."""
        mock_get.side_effect = Exception("Connection error")
        
        result = self.client.test_connection()
        self.assertFalse(result)


class TestDownloadManager(unittest.TestCase):
    """Test download manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = DownloadManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_get_download_info(self):
        """Test getting download info."""
        # Create a test file
        test_file = os.path.join(self.temp_dir, "test.mp3")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        info = self.manager.get_download_info(test_file)
        self.assertEqual(info["name"], "test.mp3")
        self.assertGreater(info["size"], 0)
        
        # Test with non-existent file
        info = self.manager.get_download_info("non_existent.mp3")
        self.assertEqual(info, {})


if __name__ == "__main__":
    unittest.main()
