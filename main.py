import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load environment variables from Railway
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Your bot's token
GUILD_ID = os.getenv("GUILD_ID")  # Your Discord Server ID
CHANNEL_ID = os.getenv("CHANNEL_ID")  # MidJourney's Discord channel ID
MIDJOURNEY_APP_ID = "1193694002684362874"  # MidJourney's official App ID

def send_imagine_command(prompt):
    url = "https://discord.com/api/v10/interactions"
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",  # ✅ Using Your Bot's Token
        "Content-Type": "application/json"
    }
    data = {
        "type": 2,  # Slash command interaction
        "application_id": MIDJOURNEY_APP_ID,  # ✅ MidJourney's App ID
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
    return jsonify({"message": "MidJourney Slash Command Automation Running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
