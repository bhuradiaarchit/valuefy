import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": 3307
}

def get_db_connection():
    """Establish a connection to MySQL with retries."""
    for attempt in range(5):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as e:
            print(f"Database connection failed (attempt {attempt + 1}): {e}")

    raise Exception("Database connection failed after multiple retries")
