import os
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

API_PATH = os.path.dirname(SCRIPT_DIR, ".openweather_apikey.txt")
DISCORD_WEBHOOK_URL_PATH = os.path.join(PROJECT_ROOT, ".discord_webhook.txt")

def weather_send():
    print("TODO")