import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch MySQL credentials from environment
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),  
    "user": os.getenv("DB_USER"),  
    "password": os.getenv("DB_PASSWORD"),  
    "database": os.getenv("DB_NAME")
}

# Ensure all required variables are set
missing_vars = [key for key, value in DB_CONFIG.items() if not value]
if missing_vars:
    raise ValueError(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
