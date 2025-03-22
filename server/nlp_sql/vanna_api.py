import requests
import json
import os
import csv
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# API endpoint and credentials
API_URL = "https://app.vanna.ai/api/v0/chat_sse"
API_KEY = os.getenv('VANNA_API_KEY')
HEADERS = {
    "Content-Type": "application/json",
    "VANNA-API-KEY": API_KEY,
    "Accept": "text/event-stream"
}

# Function to send a request and process SSE response
def get_sse_response(message):
    payload = {
        "message": message,
        "user_email": "arinzingadedrive@gmail.com",
        "acceptable_responses": ["text", "image", "link"]
    }
    
    response = requests.post(API_URL, headers=HEADERS, json=payload, stream=True)
    if response.status_code != 200:
        return {"error": f"Received status code {response.status_code}"}
    
    buffer = ""
    results = {"text": [], "images": [], "links": []}
    
    for chunk in response.iter_content(chunk_size=1):
        if not chunk:
            continue
        
        chunk_str = chunk.decode('utf-8')
        buffer += chunk_str
        
        if buffer.endswith('\n\n'):
            lines = buffer.split('\n')
            event_data = None
            
            for line in lines:
                if line.startswith('data: '):
                    event_data = line[6:]
            
            if event_data:
                try:
                    data = json.loads(event_data)
                    message_type = data.get("type")
                    
                    if message_type == "text":
                        results["text"].append(data.get("text"))
                    elif message_type == "image":
                        results["images"].append(data.get("image_url"))
                    elif message_type == "link":
                        results["links"].append({"title": data.get("title"), "url": data.get("url")})
                    elif message_type == "end":
                        break
                except json.JSONDecodeError:
                    continue
            
            buffer = ""
    
    return results

