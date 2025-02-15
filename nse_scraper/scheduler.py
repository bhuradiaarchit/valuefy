import schedule
import time
import subprocess
import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Determine Python command (Windows uses `python`, Linux/Mac may need `python3`)
PYTHON_CMD = "python" if sys.platform == "win32" else "python3"

# Get absolute path of main.py (useful if running from a different directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(BASE_DIR, "main.py")

def job():
    """Runs the scraper script."""
    logging.info("Running NSE scraper...")
    try:
        subprocess.run([PYTHON_CMD, MAIN_SCRIPT], check=True)
        logging.info("Scraper executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error while running scraper: {e}")

# Schedule the job to run at 6:00 PM every day
schedule.every().day.at("18:00").do(job)

logging.info("Scheduler is running... Waiting for the next execution...")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
