"""
Article summarization module using LLM APIs.
"""
import os
from typing import Dict, List, Optional

from strands import Agent


class ArticleSummarizer:
    """Summarizes news articles using an LLM."""
    
    def __init__(self, model: Optional[str] = None):
        """
        Initialize the article summarizer.
        
        Args:
            model: Optional model ID to use for summarization
        """
        # Initialize the Strands Agent for summarization
        self.agent = Agent(
            model=model or "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            system_prompt=(
                "You are a news article summarizer. Your task is to create concise, "
                "informative summaries of news articles in 1-2 sentences. Focus on the "
                "key facts and main points. Be objective and neutral in your summary."
            )
        )
    
    def summarize_article(self, article: Dict) -> str:
        """
        Summarize a news article using an LLM.
        
        Args:
            article: Article dictionary from NewsAPI
            
        Returns:
            String containing the article summary
        """
        # Extract article content
        title = article.get("title", "")
        description = article.get("description", "")
        content = article.get("content", "")
        
        # Create prompt for the LLM
        prompt = (
            f"Title: {title}\n"
            f"Description: {description}\n"
            f"Content: {content}\n\n"
            "Please summarize this news article in 1-2 concise sentences."
        )
        
        try:
            # Get summary from the agent
            response = self.agent(prompt)
            return response.message.strip()
        except Exception as e:
            # Fallback to simple truncation if LLM fails
            return self._fallback_summary(title, description)
    
    def _fallback_summary(self, title: str, description: str) -> str:
        """
        Create a fallback summary when LLM is unavailable.
        
        Args:
            title: Article title
            description: Article description
            
        Returns:
            Simple summary based on available text
        """
        if description:
            # Truncate description to create a simple summary
            return description[:150] + "..." if len(description) > 150 else description
        else:
            # Use title as fallback
            return title
