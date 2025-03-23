from flask import Flask, request, jsonify, render_template
from services import analyze_news  
import json  

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """Homepage that displays news recommendations on a webpage"""
    news_list = [
        {"title": "FII net buy shares worth Rs 7,470 crore", "content": "Market surging, FII buying heavily."},
        {"title": "Motilal Oswal recommends lump sum in large caps", "content": "Safe long-term bet in corrections."},
        {"title": "Rupee gains 17 paise against US Dollar", "content": "Stable forex, minor appreciation."},
        {"title": "BHEL bags Rs 7,500 cr order in Gujarat", "content": "Strong growth, revenue boost."}
    ]

    results = [analyze_news(news["title"], news["content"]) for news in news_list]

    return render_template("index.html", news_data=results)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
