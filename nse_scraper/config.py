import os
import time
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": "mysql_db",  # Matches service name in Docker
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": 3307  # Ensuring connection to MySQL on port 3307
}

def get_db_connection(retries=5, delay=5):
    """Attempts to establish a database connection with retries."""
    for attempt in range(retries):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as e:
            print(f"Database connection failed (attempt {attempt + 1}): {e}")
            time.sleep(delay)

    raise Exception("Database connection failed after multiple retries")
