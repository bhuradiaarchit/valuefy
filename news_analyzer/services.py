import os
from dotenv import load_dotenv
import groq
from config import GROQ_API_KEY
from collections import OrderedDict

load_dotenv()

# Initialize Groq client
groq_client = groq.Groq(api_key=GROQ_API_KEY)

def call_groq(prompt: str) -> str:
    """Calls Groq API to analyze news and provide a 10-word recommendation."""
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

def analyze_news(title: str, content: str) -> dict:
    """Generates a 10-word analysis and a clear BUY/SELL/HOLD recommendation."""
    
    prompt = (
        f"Analyze this financial news in exactly **10 words**, ending with 'BUY', 'SELL', or 'HOLD'.\n\n"
        f"Title: {title}\n\nContent: {content}\n\n"
        f"Output must be **exactly 10 words** followed by 'BUY/SELL/HOLD'."
    )

    recommendation = call_groq(prompt)

    return OrderedDict([
        ("title", title),
        ("content", content),
        ("recommendation", recommendation)
    ])
