from news_analyzer.services import NewsAnalyzerService
import json  
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_file
from flask_cors import CORS
import bcrypt
from sqlalchemy import create_engine
from config import get_db_connection
import psycopg2
from dotenv import load_dotenv  
from nlp_sql.in_hour_llm_to_sql import LLMtoSQL
import io
from helpers import YahooFinanceAPI, HighVolumers

app = Flask(__name__)
# Allow requests from localhost:5173
CORS(app, resources={r"/*": {"origins": "*"}})
news_service = NewsAnalyzerService()

app.secret_key = "secretkey"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "User registered successfully"}), 201

    except psycopg2.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch user from database
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        # Check if user exists
        if not user:
            return jsonify({"error": "Invalid username or password"}), 401

        # Convert stored password to bytes for bcrypt
        stored_hashed_password = user[0].encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            session["username"] = username  # Store username in session
            return jsonify({"message": "Login successful", "redirect": url_for("dashboard")}), 200

        return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template('dashboard.html', username=session["username"])
    else:
        return redirect(url_for("home"))

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


@app.route('/chat', methods = ['POST'])
def chat():
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({'error': 'Message is Required'}), 400
    
    query, df, fig = client.call_llm_to_sql(message)
    global latest_df 

    latest_df = df

    df_dict = df.to_dict() if df is not None and not df.empty else None
    fig_json = fig.to_json() if fig else None
    
    return jsonify({
        'query': query,
        'data': df_dict,
        'figure': fig_json
    })

@app.route('/analyze-news', methods=['GET'])  
def analyze_news():
   client = NewsAnalyzerService()
   news = client.execution_flow()
   
   return jsonify({'data': sanitize_json(news)})

@app.route('/download', methods=['GET'])
def download_csv():
    global latest_df

    if latest_df is None:
        return jsonify({'error': 'No data available to download'}), 400

    output = io.StringIO()
    latest_df.to_csv(output, index=False)
    output.seek(0)

    return send_file(io.BytesIO(output.getvalue().encode()), 
                     mimetype="text/csv",
                     as_attachment=True,
                     download_name="data.csv")


@app.route('/high-volumers', methods = ['GET'])
def high_volume_stocks():
    
    client = HighVolumers()
    dict_vol_table = client.execution_flow()

    return jsonify({'data': sanitize_json(dict_vol_table)})

@app.route('/gainers-losers', methods = ['GET'])
def gainers_losers():
    
    print("/gainers-losers API was called!")
    client = YahooFinanceAPI()
    dict_gainers_table = client.compare_with_latest_prices()

    return jsonify({'data': sanitize_json(dict_gainers_table)})

@app.route('/chatBot')
def chat_bot():
    return render_template('chat.html')

import math

@app.after_request
def auto_sanitize_response(response):
    if response.content_type == 'application/json':
        try:
            data = response.get_json()
            cleaned = sanitize_json(data)
            response.set_data(json.dumps(cleaned))
        except Exception as e:
            pass  # fallback if response isn't a dict
    return response


def sanitize_json(data):
    """Recursively replaces NaN, inf, -inf with None so it's safe for JSON."""
    if isinstance(data, dict):
        return {k: sanitize_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_json(i) for i in data]
    elif isinstance(data, float) and (math.isnan(data) or math.isinf(data)):
        return None
    else:
        return data


if __name__ == '__main__':
    client = LLMtoSQL()
    app.run(host='0.0.0.0', port=5000, debug=True)