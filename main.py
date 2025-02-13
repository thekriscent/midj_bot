import requests
import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load Environment Variables from Railway
USER_TOKEN = os.getenv("DISCORD_USER_TOKEN")  # ✅ Your Discord User Token
GUILD_ID = os.getenv("GUILD_ID")  # ✅ Your Discord Server ID
CHANNEL_ID = os.getenv("CHANNEL_ID")  # ✅ MidJourney's Channel ID in your server
APPLICATION_ID = "936929561302675456"  # ✅ MidJourney's Correct Application ID
COMMAND_ID = "938956540159881230"  # ✅ Correct MidJourney `/imagine` command ID
SESSION_ID = "1f7a2f96d5880b25f582d89995a73d80"  # ✅ Captured from payload
VERSION = "1237876415471554623"  # ✅ Captured from payload

def send_imagine_command(prompt):
    url = "https://discord.com/api/v10/interactions"
    headers = {
        "Authorization": f"{USER_TOKEN}",  # ✅ Using User Token
        "Content-Type": "application/json"
    }
    data = {
        "type": 2,
        "application_id": APPLICATION_ID,
        "guild_id": GUILD_ID,
        "channel_id": CHANNEL_ID,
        "session_id": SESSION_ID,
        "data": {
            "version": VERSION,
            "id": COMMAND_ID,
            "name": "imagine",
            "type": 1,
            "options": [
                {
                    "type": 3,
                    "name": "prompt",
                    "value": prompt
                }
            ],
            "application_command": {
                "id": COMMAND_ID,
                "type": 1,
                "application_id": APPLICATION_ID,
                "version": VERSION,
                "name": "imagine",
                "description": "Create images with Midjourney",
                "options": [
                    {
                        "type": 3,
                        "name": "prompt",
                        "description": "The prompt to imagine",
                        "required": True
                    }
                ],
                "dm_permission": True,
                "contexts": [0, 1, 2],
                "integration_types": [0, 1],
                "global_popularity_rank": 1
            },
            "attachments": []
        },
        "nonce": "1339447332738957312",
        "analytics_location": "slash_ui"
    }

    # Send the API request
    response = requests.post(url, headers=headers, json=data)

    # Debugging output
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)

    # Handle JSON response properly
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Failed to decode JSON", "response_text": response.text}

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
    app.run(host="0.0.0.0", port=8080, debug=True)
