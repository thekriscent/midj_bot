import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Fetch variables from Railway environment
USER_TOKEN = os.getenv("DISCORD_USER_TOKEN")  # User token (must be stored securely)
GUILD_ID = os.getenv("GUILD_ID")  # Your Discord server ID
CHANNEL_ID = os.getenv("CHANNEL_ID")  # MidJourney's Discord channel ID
APPLICATION_ID = "1193694002684362874"  # MidJourney's Application ID (fixed)

def send_imagine_command(prompt):
    url = "https://discord.com/api/v10/interactions"
    headers = {
        "Authorization": f"{USER_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": 2,  # Slash command interaction
        "application_id": APPLICATION_ID,
        "guild_id": GUILD_ID,
        "channel_id": CHANNEL_ID,
        "data": {
            "name": "imagine",
            "type": 1,
            "options": [
                {
                    "name": "prompt",
                    "type": 3,
                    "value": prompt
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

@app.route("/", methods=["POST"])
def process_request():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Invalid request, missing 'prompt'"}), 400
    
    response = send_imagine_command(data["prompt"])
    return jsonify(response), 200

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Discord MidJourney Automation Running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
