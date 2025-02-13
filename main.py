import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# ✅ Load Environment Variables from Railway
USER_TOKEN = os.getenv("DISCORD_USER_TOKEN")  # Your Discord User Token
GUILD_ID = "1193570219977887846"  # ✅ Your Discord Server ID
CHANNEL_ID = "1193570220695093330"  # ✅ Your MidJourney Channel ID
APPLICATION_ID = "936929561302675456"  # ✅ MidJourney's Application ID
COMMAND_ID = "938956540159881230"  # ✅ MidJourney `/imagine` Command ID
SESSION_ID = "1f7a2f96d5880b25f582d89995a73d80"  # ✅ Captured from Payload
VERSION = "1237876415471554623"  # ✅ Captured from Payload

# ✅ Headers (Captured from DevTools)
HEADERS = {
    "Authorization": f"{USER_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Cookie": "__Secure-recent_mfa=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3Mzk0MTg2OTYsIm5iZiI6MTczOTQxODY5NiwiZXhwIjoxNzM5NDE4OTk2LCJpc3MiOiJ1cm46ZGlzY29yZC1hcGkiLCJhdWQiOiJ1cm46ZGlzY29yZC1tZmEtcmVwcm9tcHQiLCJ1c2VyIjoxMDY2ODM1MzQ5NzIyMTA4MDI2fQ.lrOL-yeFB-nLJZxmOVj3eINIautr5rTf5dK48HIxYOSs6KgS6jh5HCUhZx154p31oWrJywLgOATY8Tq_3OeC3Q; __dcfduid=12954ba079cf11efa41db38bb083f554; __sdcfduid=12954ba179cf11efa41db38bb083f55411a80a931aa0500b5ad16e4150dd191fbb869cb5372266e9ba602d2384f10cc6; OptanonConsent=isIABGlobal=false&datestamp=Mon+Sep+23+2024+13%3A12%3A57+GMT-0400+(Eastern+Daylight+Time)&version=6.33.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1; _ga=GA1.1.1584931489.1727111577; __cfruid=2bf5e3ab21c78f6742570ad96ac6d4e6b60f7dd7-1739409832; _cfuvid=PZNL3y.XvrFMmlcGtNT9PvP0RYLgIZfqFvYadawCtfo-1739409832022-0.0.1.1-604800000; locale=en-US; _gcl_au=1.1.1651373139.1739409834; _ga_Q149DFWHT7=GS1.1.1739409833.2.0.1739409833.0.0.0; _ga_5CWMJQ1S0X=GS1.1.1739418666.3.1.1739418807.0.0.0; cf_clearance=XRWk7FpZxJpYOCvcGPUg_VXB6ppBE9m6060kX4xdHE8-1739418914-1.2.1.1-fLugqmCAKWdTec5941u.btKytXyrUM1Olmof0zVdyUDsF7NMFpvohPI3epC2zgtTppZy3.EcTu99FwswYsWPn_CujpymOig0JG6tePAZKpF3fqM1yzPDouG_UbhFkxYsjO4Hv8z56IKdbY5GYU0qDBL8yf4ZPlIcaxgOogeUvF0ttpFuf_PZ.jDDbDUOGh51SN1mlx.2IiZaSISLrkTkA_fQNgY9MChPmEtI0h_WpZ1pR4BnRPgr5w0F3qDnG3FhCMgIwYJxnrXlmFWSPMWS9aCTrfi7acAZiRSJS2bIsKc",
    "X-Super-Properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMzMuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjEzMy4wLjAuMCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjM2ODIwNSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiaGFzX2NsaWVudF9tb2RzIjpmYWxzZX0=",
    "Referer": "https://discord.com/channels/1193570219977887846/1193570220695093330"
}

def send_imagine_command(prompt):
    url = "https://discord.com/api/v10/interactions"
    
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
            ]
        }
    }

    response = requests.post(url, headers=HEADERS, json=data)
    
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)

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
