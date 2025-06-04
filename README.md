# Daily News Briefing Agent

A Strands Agent that acts as a daily news briefing assistant. This agent fetches top news headlines from NewsAPI.org based on a user-selected category, summarizes each article using an LLM, and displays the summaries in a clean and readable format.

---

## 📝 Companion to the Blog Post

This repository is a **companion project** to my blog post:  
👉 **[Building AI Agents with Amazon Q CLI and Strands MCP Server](https://community.aws/content/2xxqDr0U04YFb0LdBu0dEPWRxR4/building-ai-agents-with-amazon-q-cli-and-strands-mcp-server)**

In the blog, I walk through how I used Amazon Q Developer CLI and Strands MCP Server to configure and prompt an AI agent to generate this application.  

This repo contains the **resulting code** that was generated based on that setup.

The full configuration details and prompt engineering process are explained in the blog.

The purpose is to demonstrate how **AI-powered development workflows** can generate useful, working software through tool configuration and prompt design.

---

## Features

- Fetch top news headlines from NewsAPI.org by category
- Summarize articles using LLM (Claude via Strands Agents)
- Display results in a clean CLI format with rich formatting
- Option to generate HTML output
- Schedule daily runs using Python scheduler or crontab
- Interactive mode with a Strands Agent for natural language interaction

## Requirements

- Python 3.8+
- NewsAPI.org API key (get one at [https://newsapi.org](https://newsapi.org))
- AWS credentials configured (for Bedrock access) or other LLM API access

## Installation

1. Clone this repository or download the source code
2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. (Optional) Create a `.env` file in the project directory with your NewsAPI.org API key:

```
NEWS_API_KEY=your_api_key_here
```

## Usage

### Command Line Interface

Run the agent with the CLI:

```bash
python agent.py [CATEGORY] [OPTIONS]
```

Arguments:
- `CATEGORY`: News category (business, entertainment, general, health, science, sports, technology)

Options:
- `--api-key`, `-k`: NewsAPI.org API key (if not provided, will check environment or prompt)
- `--html`, `-h`: Output results as HTML
- `--schedule`, `-s`: Schedule daily run at specified time (24-hour format, e.g., '08:00')
- `--cron`: Use crontab instead of Python scheduler

Examples:

```bash
# Fetch technology news
python agent.py technology

# Fetch business news and generate HTML output
python agent.py business --html

# Schedule daily sports news briefing at 8:00 AM
python agent.py sports --schedule "08:00"

# Generate crontab entry for daily health news at 7:30 AM
python agent.py health --schedule "07:30" --cron
```

### Interactive Strands Agent

For a more conversational experience, use the Strands Agent interface:

```bash
python strands_agent.py
```

This starts an interactive session where you can chat with the news briefing agent using natural language.

## Project Structure

- `agent.py`: Main CLI application
- `strands_agent.py`: Interactive Strands Agent implementation
- `news_api.py`: NewsAPI.org client
- `summarizer.py`: Article summarization using LLM
- `formatter.py`: Output formatting for CLI and HTML
- `scheduler.py`: Scheduling functionality

## Customization

- To use a different LLM model, modify the model ID in `agent.py` and `strands_agent.py`
- To change the number of articles fetched, modify the `page_size` parameter in `news_api.py`
- To customize the HTML output, modify the HTML template in `formatter.py`

## License

MIT
