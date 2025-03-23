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
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing from environment variables.")

        self.groq_client = groq.Groq(api_key=GROQ_API_KEY)

    def call_groq(self, prompt: str) -> str:
        """Calls Groq API to analyze news and provide a 10-word recommendation."""
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"

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
    

    def execution_flow(self):
        news_list = [
            {
                "title": "FII net buy shares worth Rs 7,470 crore and DIIs net sellers of Rs 3,202 crore",
                "content": "In today's session, the market’s fiery run continued, with the Nifty locking in its best weekly performance in four years, soaring 4.27 percent — the highest since February 2021, when it had surged 9.46 percent in a week. The Sensex wasn’t far behind, posting its best week since July 2022, with a 4.2 percent gain that underscored the market’s unrelenting momentum."
            },
            {
                "title": "Motilal Oswal recommends lump sum investment in hybrid, large cap funds",
                "content": "Motilal Oswal Private Wealth advises a lump sum investment strategy in Hybrid and Large Cap funds amid recent market corrections. A staggered approach is suggested for Flexi, Mid, and Small Cap funds."
            },
            {
                "title": "Rupee Gains 17 Paise to ₹86.19 Against US Dollar Amid Positive Market Sentiment",
                "content": "The Indian rupee appreciated by 17 paise to ₹86.19 against the US dollar in early trade"
            },  
            {
                "title": "1.91 lakh circuit km transmission lines to be added by 2032",
                "content": "The expansion, detailed in the National Electricity Plan, aims to meet the country's growing electricity demand and ensure optimal usage of generating capacity."
            },
            {
                "title": "BHEL bags Rs 7,500 cr order to set up 800 MW unit at Ukai plant, in Gujarat",
                "content": "BHEL has secured an order under international competitive bidding, for setting up a 1x800 MW Ukai supercritical thermal power plant (Unit-7) on an Engineering, Procurement & Construction (EPC) basis, in Tapi district, Gujarat."
            }
        ]

        results = [self.analyze_single_news(news["title"], news["content"]) for news in news_list]

        return results


if __name__ == "__main__":
    client = NewsAnalyzerService()
    news = client.execution_flow()

    print(news)