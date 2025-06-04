"""
Scheduling functionality for the news briefing agent.
"""
import os
import time
import schedule
import subprocess
from typing import Optional
from datetime import datetime


class NewsScheduler:
    """Handles scheduling of news briefing runs."""
    
    def __init__(self, script_path: str):
        """
        Initialize the news scheduler.
        
        Args:
            script_path: Path to the main script to run
        """
        self.script_path = script_path
    
    def schedule_daily(self, time_str: str, category: str, api_key: str) -> None:
        """
        Schedule a daily news briefing.
        
        Args:
            time_str: Time to run in 24-hour format (e.g., "08:00")
            category: News category to fetch
            api_key: NewsAPI.org API key
        """
        def job():
            """Run the news briefing script."""
            print(f"Running scheduled news briefing for {category} at {datetime.now()}")
            subprocess.run(["python", self.script_path, category, "--api-key", api_key])
        
        # Schedule the job
        schedule.every().day.at(time_str).do(job)
        print(f"Scheduled daily news briefing for {category} at {time_str}")
        
        try:
            # Keep the scheduler running
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("Scheduler stopped.")
    
    @staticmethod
    def setup_cron_job(time_str: str, category: str, api_key: str) -> str:
        """
        Generate a crontab entry for scheduling.
        
        Args:
            time_str: Time to run in 24-hour format (e.g., "08:00")
            category: News category to fetch
            api_key: NewsAPI.org API key
            
        Returns:
            String with crontab command to set up scheduling
        """
        # Parse the time string
        hour, minute = time_str.split(":")
        
        # Get the absolute path to the current script
        script_path = os.path.abspath("agent.py")
        
        # Generate the crontab entry
        cron_entry = f"{minute} {hour} * * * cd {os.path.dirname(script_path)} && python {script_path} {category} --api-key {api_key}"
        
        # Generate the command to add this to crontab
        crontab_cmd = f"(crontab -l 2>/dev/null; echo '{cron_entry}') | crontab -"
        
        return crontab_cmd
