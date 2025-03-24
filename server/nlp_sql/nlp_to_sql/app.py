from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import sqlite3
from llama_cpp import Llama

app = Flask(__name__)
CORS(app)  # Allows frontend to access the backend

# Load Llama model
llm = Llama(model_path="models/llama-2-7b.Q4_K_M.gguf")

# Database connection function
def get_db_connection():
    conn = sqlite3.connect("database/database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@app.route('/')
def index():
    return render_template("index.html")

# API route to process user query
@app.route('/generate_sql', methods=['POST'])
def generate_sql():
    data = request.json
    user_query = data.get("query")

    # Generate SQL query using Llama
    response = llm(f"Convert this into SQL: {user_query}")
    sql_query = response["choices"][0]["text"]

    # Store in the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO queries (user_query, sql_query) VALUES (?, ?)", (user_query, sql_query))
    conn.commit()
    conn.close()

    return jsonify({"sql_query": sql_query})

if __name__ == '__main__':
    app.run(debug=True)
