"""
Strands Agent implementation for the news briefing assistant.

This file defines a Strands Agent that can be used to interact with the news briefing
functionality through natural language.
"""
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

from strands import Agent, tool
from news_api import NewsAPIClient
from summarizer import ArticleSummarizer
from formatter import NewsFormatter

# Load environment variables
load_dotenv()


@tool
def get_news_categories() -> List[str]:
    """
    Get available news categories.
    
    Returns:
        List of available news categories
    """
    return NewsAPIClient.get_available_categories()


@tool
def fetch_news_headlines(category: str, api_key: str, count: int = 5) -> List[Dict]:
    """
    Fetch top news headlines for a specific category.
    
    Args:
        category: News category (business, entertainment, general, health, 
                science, sports, technology)
        api_key: NewsAPI.org API key
        count: Number of articles to fetch (default: 5)
        
    Returns:
        List of news articles
    """
    # Initialize the NewsAPI client
    news_client = NewsAPIClient(api_key)
    
    # Fetch top headlines
    response = news_client.get_top_headlines(category=category, page_size=count)
    
    # Extract articles
    articles = news_client.extract_articles(response)
    
    return articles


@tool
def summarize_news_articles(articles: List[Dict]) -> List[str]:
    """
    Summarize a list of news articles.
    
    Args:
        articles: List of news articles from NewsAPI
        
    Returns:
        List of article summaries
    """
    # Initialize the summarizer
    summarizer = ArticleSummarizer()
    
    # Summarize each article
    summaries = []
    for article in articles:
        summary = summarizer.summarize_article(article)
        summaries.append(summary)
    
    return summaries


@tool
def format_news_briefing(articles: List[Dict], category: str, summaries: List[str]) -> str:
    """
    Format news articles with their summaries as a text briefing.
    
    Args:
        articles: List of news articles
        category: News category
        summaries: List of article summaries
        
    Returns:
        Formatted text briefing
    """
    briefing = f"Daily News Briefing - {category.title()}\n\n"
    
    for i, (article, summary) in enumerate(zip(articles, summaries), 1):
        title = article.get("title", "No title")
        source = article.get("source", {}).get("name", "Unknown source")
        url = article.get("url", "")
        
        briefing += f"#{i}: {title}\n"
        briefing += f"{summary}\n"
        briefing += f"Source: {source} - {url}\n\n"
    
    return briefing


@tool
def save_news_briefing_html(articles: List[Dict], category: str, summaries: List[str]) -> str:
    """
    Save news briefing as HTML file.
    
    Args:
        articles: List of news articles
        category: News category
        summaries: List of article summaries
        
    Returns:
        Path to saved HTML file
    """
    formatter = NewsFormatter()
    html_content = formatter.generate_html(articles, category, summaries)
    html_path = formatter.save_html_to_file(html_content, category)
    return html_path


def create_news_briefing_agent() -> Agent:
    """
    Create and configure the news briefing Strands Agent.
    
    Returns:
        Configured Strands Agent
    """
    # Create the agent with our custom tools
    agent = Agent(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        tools=[
            get_news_categories,
            fetch_news_headlines,
            summarize_news_articles,
            format_news_briefing,
            save_news_briefing_html
        ],
        system_prompt=(
            "You are a helpful news briefing assistant. Your job is to fetch news headlines "
            "based on user preferences, summarize them, and present them in a clean format. "
            "You should be concise, informative, and neutral in your presentation of news.\n\n"
            "You can help users get the latest news in various categories, summarize articles, "
            "and save briefings as HTML files. You should guide users through the process of "
            "selecting a category and providing their NewsAPI.org API key if needed.\n\n"
            "Always be respectful of user privacy and never store API keys permanently."
        )
    )
    
    return agent


if __name__ == "__main__":
    # Create the agent
    news_agent = create_news_briefing_agent()
    
    # Get API key from environment or ask user
    api_key = os.environ.get("NEWS_API_KEY")
    
    # Initial message to the agent
    initial_message = (
        "Hello! I'm your news briefing assistant. I can help you get the latest news "
        "headlines in various categories, summarize them, and present them in a clean format.\n\n"
        "To get started, please tell me what news category you're interested in "
        "(business, entertainment, general, health, science, sports, or technology)."
    )
    
    print(initial_message)
    
    # Interactive loop
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Exit condition
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nThank you for using the news briefing assistant. Goodbye!")
            break
        
        # Process with the agent
        response = news_agent(user_input)
        
        # Print the response
        print(f"\nNews Assistant: {response.message}")
