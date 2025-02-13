import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load Environment Variables from Railway
USER_TOKEN = os.getenv("DISCORD_USER_TOKEN")  # Your personal Discord User Token
GUILD_ID = os.getenv("GUILD_ID")  # Your Discord Server ID
CHANNEL_ID = os.getenv("CHANNEL_ID")  # MidJourney's Channel ID in your server
APPLICATION_ID = "1193694002684362874"  # ✅ Correct MidJourney Application ID

def send_imagine_command(prompt):
    url = "https://discord.com/api/v10/interactions"
    headers = {
        "Authorization": f"Bot {USER_TOKEN}",  # ✅ Using Bot Token
        "Content-Type": "application/json"
    }
    data = {
        "type": 2,  # Slash command interaction
        "application_id": APPLICATION_ID,  # ✅ Correct MidJourney Application ID
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
