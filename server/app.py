from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv
from config import get_db_connection

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Ensure this is set in your .env file

# Ensure users table exists
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

initialize_database()

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password.decode("utf-8")))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409
    finally:
        cursor.close()
        conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode("utf-8"), user[0].encode("utf-8")):
        session["user"] = username
        return jsonify({"redirect": url_for("dashboard")})

    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))
    return render_template("dashboard.html", username=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
