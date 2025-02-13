import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Use your User Token from Railway variables
USER_TOKEN = os.getenv("DISCORD_USER_TOKEN")  
CHANNEL_ID = "1193570220695093330"  # Replace with your MidJourney channel ID

def send_message(prompt):
    url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"{USER_TOKEN}",  # Uses your User Token
        "Content-Type": "application/json"
    }
    data = {
        "content": f"/imagine prompt: {prompt}"
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

@app.route("/", methods=["POST"])
def process_request():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Invalid request, missing 'prompt'"}), 400
    
    response = send_message(data["prompt"])
    return jsonify(response), 200

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Discord User Automation Running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
