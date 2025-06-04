"""
News Briefing Agent using Strands Agents.

This agent fetches top news headlines from NewsAPI.org based on a user-selected category,
summarizes each article using an LLM, and displays the summaries in a clean format.
"""
import os
import sys
import typer
from typing import Optional
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt, Confirm

from strands import Agent, tool
from news_api import NewsAPIClient
from summarizer import ArticleSummarizer
from formatter import NewsFormatter
from scheduler import NewsScheduler

# Initialize console for rich output
console = Console()

# Load environment variables from .env file if it exists
load_dotenv()

# Create the CLI app
app = typer.Typer(help="Daily News Briefing Agent")


@tool
def fetch_news(category: str, api_key: str) -> list:
    """
    Fetch top news headlines for a specific category.
    
    Args:
        category: News category (business, entertainment, general, health, 
                science, sports, technology)
        api_key: NewsAPI.org API key
        
    Returns:
        List of news articles
    """
    try:
        # Initialize the NewsAPI client
        news_client = NewsAPIClient(api_key)
        
        # Fetch top headlines
        response = news_client.get_top_headlines(category=category)
        
        # Extract articles
        articles = news_client.extract_articles(response)
        
        return articles
    except Exception as e:
        console.print(f"[bold red]Error fetching news: {str(e)}[/bold red]")
        return []


@tool
def summarize_articles(articles: list) -> list:
    """
    Summarize a list of news articles.
    
    Args:
        articles: List of news articles from NewsAPI
        
    Returns:
        List of article summaries
    """
    try:
        # Initialize the summarizer
        summarizer = ArticleSummarizer()
        
        # Summarize each article
        summaries = []
        with console.status("[bold green]Summarizing articles...") as status:
            for i, article in enumerate(articles):
                console.print(f"Summarizing article {i+1}/{len(articles)}")
                summary = summarizer.summarize_article(article)
                summaries.append(summary)
        
        return summaries
    except Exception as e:
        console.print(f"[bold red]Error summarizing articles: {str(e)}[/bold red]")
        return ["Unable to generate summary." for _ in articles]


@tool
def display_news(articles: list, category: str, summaries: list, output_html: bool = False) -> Optional[str]:
    """
    Display news articles with their summaries.
    
    Args:
        articles: List of news articles
        category: News category
        summaries: List of article summaries
        output_html: Whether to output HTML (default: False)
        
    Returns:
        Path to HTML file if output_html is True, None otherwise
    """
    try:
        # Initialize the formatter
        formatter = NewsFormatter()
        
        # Display in CLI
        formatter.format_cli_output(articles, category, summaries)
        
        # Generate HTML if requested
        if output_html:
            html_content = formatter.generate_html(articles, category, summaries)
            html_path = formatter.save_html_to_file(html_content, category)
            console.print(f"[bold green]HTML output saved to: {html_path}[/bold green]")
            return html_path
        
        return None
    except Exception as e:
        console.print(f"[bold red]Error displaying news: {str(e)}[/bold red]")
        return None


def create_news_agent() -> Agent:
    """
    Create and configure the news briefing agent.
    
    Returns:
        Configured Strands Agent
    """
    # Create the agent with our custom tools
    agent = Agent(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        tools=[fetch_news, summarize_articles, display_news],
        system_prompt=(
            "You are a helpful news briefing assistant. Your job is to fetch news headlines "
            "based on user preferences, summarize them, and present them in a clean format. "
            "You should be concise, informative, and neutral in your presentation of news."
        )
    )
    
    return agent


@app.command()
def run(
    category: Optional[str] = typer.Argument(
        None, 
        help="News category (business, entertainment, general, health, science, sports, technology)"
    ),
    api_key: Optional[str] = typer.Option(
        None, 
        "--api-key", 
        "-k", 
        help="NewsAPI.org API key"
    ),
    output_html: bool = typer.Option(
        False, 
        "--html", 
        "-h", 
        help="Output results as HTML"
    ),
    schedule_time: Optional[str] = typer.Option(
        None, 
        "--schedule", 
        "-s", 
        help="Schedule daily run at specified time (24-hour format, e.g., '08:00')"
    ),
    use_cron: bool = typer.Option(
        False, 
        "--cron", 
        help="Use crontab instead of Python scheduler"
    )
):
    """Run the news briefing agent to fetch and summarize news articles."""
    # Get available categories
    available_categories = NewsAPIClient.get_available_categories()
    
    # Prompt for category if not provided
    if not category:
        category = Prompt.ask(
            "Select a news category", 
            choices=available_categories,
            default="technology"
        )
    
    # Validate category
    if category not in available_categories:
        console.print(f"[bold red]Invalid category: {category}[/bold red]")
        console.print(f"Available categories: {', '.join(available_categories)}")
        sys.exit(1)
    
    # Get API key from argument, environment, or prompt
    if not api_key:
        api_key = os.environ.get("NEWS_API_KEY")
        
    if not api_key:
        api_key = Prompt.ask("Enter your NewsAPI.org API key", password=True)
    
    # If scheduling is requested
    if schedule_time:
        if use_cron:
            # Generate crontab command
            scheduler = NewsScheduler(os.path.abspath(__file__))
            cron_cmd = scheduler.setup_cron_job(schedule_time, category, api_key)
            
            # Display the command
            console.print(f"[bold]Run this command to schedule with crontab:[/bold]")
            console.print(f"[green]{cron_cmd}[/green]")
            
            # Ask if user wants to run it now
            if Confirm.ask("Do you want to run this command now?"):
                os.system(cron_cmd)
                console.print("[bold green]Cron job scheduled successfully![/bold green]")
        else:
            # Use Python scheduler
            console.print(f"[bold]Scheduling daily news briefing for {category} at {schedule_time}[/bold]")
            console.print("[italic]Press Ctrl+C to stop the scheduler[/italic]")
            
            scheduler = NewsScheduler(os.path.abspath(__file__))
            scheduler.schedule_daily(schedule_time, category, api_key)
    else:
        # Run the news briefing now
        console.print(f"[bold]Fetching {category} news...[/bold]")
        
        # Fetch news
        articles = fetch_news(category, api_key)
        
        if not articles:
            console.print("[bold red]No articles found.[/bold red]")
            sys.exit(1)
        
        console.print(f"[bold green]Found {len(articles)} articles.[/bold green]")
        
        # Summarize articles
        summaries = summarize_articles(articles)
        
        # Display results
        display_news(articles, category, summaries, output_html)


if __name__ == "__main__":
    app()
