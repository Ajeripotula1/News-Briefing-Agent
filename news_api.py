"""
News API client for fetching news headlines.
"""
import os
import requests
from typing import Dict, List, Optional


class NewsAPIClient:
    """Client for interacting with NewsAPI.org."""
    
    BASE_URL = "https://newsapi.org/v2"
    
    def __init__(self, api_key: str):
        """
        Initialize the NewsAPI client.
        
        Args:
            api_key: NewsAPI.org API key
        """
        self.api_key = api_key
        
    def get_top_headlines(self, 
                         category: str, 
                         country: str = "us", 
                         page_size: int = 5) -> Dict:
        """
        Fetch top headlines from NewsAPI.org.
        
        Args:
            category: News category (business, entertainment, general, health, 
                     science, sports, technology)
            country: 2-letter ISO 3166-1 country code (default: "us")
            page_size: Number of results to return (default: 5)
            
        Returns:
            Dict containing the API response
        """
        endpoint = f"{self.BASE_URL}/top-headlines"
        
        params = {
            "apiKey": self.api_key,
            "category": category,
            "country": country,
            "pageSize": page_size
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        return response.json()
    
    @staticmethod
    def extract_articles(response: Dict) -> List[Dict]:
        """
        Extract article data from the API response.
        
        Args:
            response: NewsAPI response dictionary
            
        Returns:
            List of article dictionaries
        """
        if response.get("status") != "ok":
            raise ValueError(f"API Error: {response.get('message', 'Unknown error')}")
        
        return response.get("articles", [])
    
    @staticmethod
    def get_available_categories() -> List[str]:
        """
        Get list of available news categories.
        
        Returns:
            List of category strings
        """
        return [
            "business", 
            "entertainment", 
            "general", 
            "health", 
            "science", 
            "sports", 
            "technology"
        ]
