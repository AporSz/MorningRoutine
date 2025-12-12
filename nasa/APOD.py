import os
import requests

# Get the folder where this script is actually located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Construct absolute paths to your keys
NASA_API_PATH = os.path.join(SCRIPT_DIR, ".nasaAPI.txt")
DISCORD_WEBHOOK_URL_PATH = os.path.join(PROJECT_ROOT, ".discord_webhook.txt")

def get_secret(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: Could not find secret file at {filepath}")
        return None


def get_earth_image():
    print("--- Starting NASA APOD Bot ---")

    # 1. Get API Key
    NASA_API_KEY = get_secret(NASA_API_PATH)
    if not NASA_API_KEY:
        print("CRITICAL: NASA API key missing. Exiting.")
        return

    # 2. Fetch Metadata
    print("Contacting NASA API...")
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises error if status != 200
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to NASA: {e}")
        return

    data = response.json()

    # 3. Parse Data
    title = data.get("title", "No Title")
    date = data.get("date", "Unknown Date")
    explanation = data.get("explanation", "No explanation.")

    img_url = data.get("hdurl")

    if not img_url:
        print("No image URL found in response.")
        return

    print(f"Found image: {title}")

    # 4. Send the LINK (Instant speed)
    send_to_discord(img_url, title, date, explanation)


def send_to_discord(image_url, title, date_text, explanation):
    print("Sending Link to Discord...")

    # 1. Get Webhook
    DISCORD_WEBHOOK_URL = get_secret(DISCORD_WEBHOOK_URL_PATH)
    if not DISCORD_WEBHOOK_URL:
        print("CRITICAL: Discord Webhook URL missing. Exiting.")
        return

    # 2. Build Rich Embed Payload
    # This displays the image nicely without downloading it
    payload = {
        "username": "NASA Bot",
        "embeds": [
            {
                "title": f"{title}",
                "description": f"**{date_text}**\n\n{explanation[:1000]}...",
                "image": {
                    "url": image_url
                },
                "color": 0x0B3D91  # NASA Blue
            }
        ]
    }

    # 3. Post
    try:
        result = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        result.raise_for_status()
        print("Success! Payload delivered to Discord.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send to Discord: {e}")


def apod_send():
    get_earth_image()