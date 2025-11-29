#!/usr/bin/env python3
"""
Lexicon API client implementation
"""

import requests
import logging
from typing import Dict, Any, Optional, List
from error_handler import LexiconError

logger = logging.getLogger(__name__)


class LexiconClient:
    """Client for interacting with the Lexicon API."""
    
    def __init__(self, base_url: str = "http://localhost:48624/v1"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def test_connection(self) -> bool:
        """Test connection to the Lexicon API."""
        try:
            response = self.session.get(f"{self.base_url}/tracks", timeout=5)
            return response.status_code == 200
        except requests.RequestException as e:
            logger.error(f"Error testing Lexicon connection: {e}")
            return False
    
    def add_track(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Add a track to the Lexicon library.
        
        Args:
            file_path: Path to the audio file to add
            
        Returns:
            Dictionary with track data if successful, None otherwise
            
        Raises:
            LexiconError: If there's an error adding the track
        """
        try:
            data = {"locations": [file_path]}
            response = self.session.post(
                f"{self.base_url}/track",
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("data", {}).get("track")
            else:
                error_msg = f"Error adding track: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise LexiconError(error_msg)
                
        except requests.RequestException as e:
            error_msg = f"Error adding track to Lexicon: {e}"
            logger.error(error_msg)
            raise LexiconError(error_msg)
    
    def get_track(self, track_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a track from the Lexicon library by ID.
        
        Args:
            track_id: ID of the track to retrieve
            
        Returns:
            Dictionary with track data if successful, None otherwise
            
        Raises:
            LexiconError: If there's an error getting the track
        """
        try:
            response = self.session.get(
                f"{self.base_url}/track",
                params={"id": track_id},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get("data", {}).get("track")
            else:
                error_msg = f"Error getting track: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise LexiconError(error_msg)
                
        except requests.RequestException as e:
            error_msg = f"Error getting track from Lexicon: {e}"
            logger.error(error_msg)
            raise LexiconError(error_msg)
    
    def search_tracks(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for tracks in the Lexicon library.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of track dictionaries
            
        Raises:
            LexiconError: If there's an error searching tracks
        """
        try:
            # Simple search by title or artist
            data = {
                "filter": {
                    "title": query
                },
                "limit": limit
            }
            
            response = self.session.get(
                f"{self.base_url}/search/tracks",
                params=data,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get("data", {}).get("tracks", [])
            else:
                error_msg = f"Error searching tracks: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise LexiconError(error_msg)
                
        except requests.RequestException as e:
            error_msg = f"Error searching tracks in Lexicon: {e}"
            logger.error(error_msg)
            raise LexiconError(error_msg)


def test_lexicon_connection(base_url: str = "http://localhost:48624/v1") -> bool:
    """
    Test connection to the Lexicon API.
    
    Args:
        base_url: Base URL of the Lexicon API
        
    Returns:
        True if connection is successful, False otherwise
    """
    client = LexiconClient(base_url)
    return client.test_connection()
