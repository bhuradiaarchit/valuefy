import os
import json
from dotenv import load_dotenv
import groq
from collections import OrderedDict

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class NewsAnalyzerService:
    """Service for analyzing financial news using the Groq API."""

    def __init__(self):
        """Initialize the Groq client."""
        self.groq_client = groq.Groq(api_key=GROQ_API_KEY)

    def call_groq(self, prompt: str) -> str:
        """Calls Groq API to analyze news and provide a 10-word recommendation."""
        chat_completion = self.groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content

    def analyze_single_news(self, title: str, content: str) -> dict:
        """Analyzes a single news article and returns a recommendation."""
        prompt = (
            f"Analyze this financial news in exactly **10 words**, ending with 'BUY', 'SELL', or 'HOLD'.\n\n"
            f"Title: {title}\n\nContent: {content}\n\n"
            f"Output must be **exactly 10 words** followed by 'BUY/SELL/HOLD'."
        )

        recommendation = self.call_groq(prompt)

        return OrderedDict([
            ("title", title),
            ("content", content),
            ("recommendation", recommendation)
        ])

    def analyze_multiple_news(self) -> dict:
        """Analyzes predefined financial news articles and returns recommendations in JSON format."""
        news_list = [
            {"title": "FII net buy shares worth Rs 7,470 crore", "content": "Market surging, FII buying heavily."},
            {"title": "Motilal Oswal recommends lump sum in large caps", "content": "Safe long-term bet in corrections."},
            {"title": "Rupee gains 17 paise against US Dollar", "content": "Stable forex, minor appreciation."},
            {"title": "BHEL bags Rs 7,500 cr order in Gujarat", "content": "Strong growth, revenue boost."}
        ]

        results = [self.analyze_single_news(news["title"], news["content"]) for news in news_list]

        # Convert to JSON and return
        return json.dumps(results, indent=4)
