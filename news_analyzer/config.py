import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("⚠️ Error: GROQ_API_KEY is missing in the .env file")
