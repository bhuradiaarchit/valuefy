from flask import Flask, request, jsonify
from services import analyze_news  
import json 

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """Homepage that displays sample news analysis for multiple news articles"""
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

    results = [analyze_news(news["title"], news["content"]) for news in news_list]

    return app.response_class(
        response=json.dumps(results, indent=4, ensure_ascii=False, sort_keys=False),
        mimetype="application/json"
    )

@app.route("/analyze-news", methods=["POST"])
def get_news_analysis():
    """API endpoint to analyze news dynamically"""
    data = request.get_json()

    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Missing title or content"}), 400

    result = analyze_news(data["title"], data["content"])
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
