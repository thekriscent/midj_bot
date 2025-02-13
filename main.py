import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = "1193570220695093330"  # Replace with your MidJourney Discord channel ID
APPLICATION_ID = "YOUR_MIDJOURNEY_APP_ID"  # Replace with MidJourney's Discord App ID

def send_slash_command(prompt):
    url = f"https://discord.com/api/v10/interactions"
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": 2,  # Slash command interaction
        "application_id": APPLICATION_ID,
        "guild_id": "YOUR_SERVER_ID",  # Replace with your Discord Server ID
        "channel_id": CHANNEL_ID,
        "data": {
            "name": "imagine",
            "options": [{"name": "prompt", "value": prompt}]
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print("Discord API Response:", response.status_code, response.text)  # Debugging line
    return response.json()

@app.route("/", methods=["POST"])
def process_request():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Invalid request, missing 'prompt'"}), 400
    
    response = send_slash_command(data["prompt"])
    return jsonify(response), 200

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Discord Bot Running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
