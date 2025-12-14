import os
import requests
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

API_PATH = os.path.join(SCRIPT_DIR, ".openweather_apikey.txt")
DISCORD_WEBHOOK_URL_PATH = os.path.join(PROJECT_ROOT, ".discord_webhook.txt")

def get_secret(path):
    try:
        with open(path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Coulnd find file with path: {path}")
        return None


def weather_get(long, lat):
    API_KEY = get_secret(API_PATH)
    if API_KEY is None:
        print("Error getting API key")
        return

    print("Getting weather data")
    URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={long}&lon={lat}&units=metric&appid={API_KEY}"

    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to OpenWeather: {e}")
        return

    data = response.json()
    time = date.fromtimestamp(data.get("current", None).get("dt", None))
    sunrise = data.get("current", None).get("sunrise", None)
    sunset = data.get("current", None).get("sunset", None)
    c_temperature = data.get("current", None).get("temp", None)
    c_feelslike = data.get("current", None).get("feels_like", None)
    c_humidity = data.get("current", None).get("humidity", None)
    c_uvindex = data.get("current", None).get("uvi", None)
    c_clouds = data.get("current", None).get("clouds", None)
    c_visibility = data.get("current", None).get("visibility", None)
    c_windspeed = data.get("current", None).get("wind_speed", None)
    c_weather = data.get("current", None).get("weather", None)[0].get("main", None)
    c_weather_desc = data.get("current", None).get("weather", None)[0].get("description", None)

    print(time)
    print(c_temperature)
    print(c_weather_desc)

# TODO: long and lat settings
def weather_send():
    print("TODO")

# DOX WARNING!
# 46.763064, 23.619588

weather_get(46.763064,23.619588)