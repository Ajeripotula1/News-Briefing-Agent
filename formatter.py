"""
Output formatting for news briefings.
"""
import os
from typing import Dict, List
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class NewsFormatter:
    """Formats news articles for display."""
    
    def __init__(self):
        """Initialize the news formatter."""
        self.console = Console()
    
    def format_cli_output(self, articles: List[Dict], category: str, summaries: List[str]) -> None:
        """
        Format and display news articles in the CLI.
        
        Args:
            articles: List of article dictionaries
            category: News category
            summaries: List of article summaries
        """
        # Create header
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        self.console.print(f"\n[bold cyan]Daily News Briefing - {category.title()}[/bold cyan]")
        self.console.print(f"[italic]{current_date}[/italic]\n")
        
        # Display each article
        for i, (article, summary) in enumerate(zip(articles, summaries), 1):
            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown source")
            url = article.get("url", "")
            
            panel = Panel(
                f"[bold]{title}[/bold]\n\n"
                f"[italic]{summary}[/italic]\n\n"
                f"Source: {source}\n"
                f"[link={url}]Read more[/link]",
                title=f"[bold white]#{i}[/bold white]",
                border_style="blue"
            )
            self.console.print(panel)
            self.console.print("")  # Add spacing between articles
    
    def generate_html(self, articles: List[Dict], category: str, summaries: List[str]) -> str:
        """
        Generate HTML output for news articles.
        
        Args:
            articles: List of article dictionaries
            category: News category
            summaries: List of article summaries
            
        Returns:
            HTML string representation of the news briefing
        """
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily News Briefing - {category.title()}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .date {{
            color: #7f8c8d;
            font-style: italic;
            margin-bottom: 20px;
        }}
        .article {{
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .article h2 {{
            margin-top: 0;
            color: #2980b9;
        }}
        .summary {{
            font-style: italic;
            color: #34495e;
            margin: 10px 0;
        }}
        .source {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>Daily News Briefing - {category.title()}</h1>
    <div class="date">{current_date}</div>
"""
        
        for i, (article, summary) in enumerate(zip(articles, summaries), 1):
            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown source")
            url = article.get("url", "")
            
            html += f"""
    <div class="article">
        <h2>{title}</h2>
        <div class="summary">{summary}</div>
        <div class="source">
            Source: {source} - <a href="{url}" target="_blank">Read more</a>
        </div>
    </div>
"""
        
        html += """
</body>
</html>
"""
        return html
    
    def save_html_to_file(self, html_content: str, category: str) -> str:
        """
        Save HTML content to a file.
        
        Args:
            html_content: HTML string to save
            category: News category for filename
            
        Returns:
            Path to the saved HTML file
        """
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/news_briefing_{category}_{timestamp}.html"
        
        # Write HTML to file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return filename
