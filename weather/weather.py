import os

import requests
from datetime import datetime
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

API_PATH = os.path.join(SCRIPT_DIR, ".openweather_apikey.txt")
DISCORD_WEBHOOK_URL_PATH = os.path.join(PROJECT_ROOT, ".discord_webhook.txt")
DEFAULT_COORDINATES = os.path.join(SCRIPT_DIR, ".default_location.txt")


if len(sys.argv) != 3:
    print("Using default coordinates")
    try:
        with open(DEFAULT_COORDINATES, "r") as file:
            latitude = float(file.readline().strip())
            longitude = float(file.readline().strip())
    except FileNotFoundError:
        print(f"Couldn't find file with coordinates: {DEFAULT_COORDINATES}")
        exit(1)
else:
    longitude = float(sys.argv[1])
    latitude = float(sys.argv[2])

def get_secret(path):
    try:
        with open(path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Coulnd find file with path: {path}")
        return None

def icons(icon_id):
    icon_map = {
        "01d": "<:01d:1450470171838775346>",
        "01n": "<:01n:1450470236825456802>",

        "02d": "<:02d:1450470299031310347>",
        "02n": "<:02n:1450470338789117982>",

        "03d": "<:03d:1450470413523226668>",
        "03n": "<:03n:1450470464928350398>",

        "04d": "<:04d:1450470510008733888>",
        "04n": "<:04n:1450470560155963564>",

        "09d": "<:09d:1450470607350137058>",
        "09n": "<:09n:1450470658659188858>",

        "10d": "<:10d:1450470719552098425>",
        "10n": "<:10n:1450470758378635389>",

        "11d": "<:11d:1450470802180014100>",
        "11n": "<:11n:1450470843590115389>",

        "13d": "<:13d:1450470889983578133>",
        "13n": "<:13n:1450470928638279702>",

        "50d": "<:50d:1450470981977116745>",
        "50n": "<:50n:1450471021478936586>",
    }
    return icon_map[icon_id]


def generate_hourly(hourly):
    prediction_text = ""
    for item in hourly:
        prediction_text += f"- **{datetime.fromtimestamp(item.get("dt", None)).time().hour}**: {icons(item.get("weather", None)[0].get("icon", None))} temp: **{item.get("temp", None)}°C** feels like {item.get("feels_like", None)}°C\n"

    return prediction_text

def weather_get_and_send():
    API_KEY = get_secret(API_PATH)
    if API_KEY is None:
        print("Error getting API key")
        return

    print("Getting weather data")
    URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&units=metric&appid={API_KEY}"

    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to OpenWeather: {e}")
        return

    data = response.json()
    time = datetime.fromtimestamp(data.get("current", None).get("dt", None))
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
    alerts = data.get("alerts", None)

    minutely = data.get("minutely", None)
    will_it_rain = False
    rain_start = 0

    for i in range(0, 59):
        if minutely[i].get("precipitation", None) > 0:
            will_it_rain = True
            rain_start = i

    prediction_text = ""
    prediction_text += f"### {c_weather_desc}, {c_temperature} degrees Celsius, which feel like {c_feelslike} \n"

    if alerts is not None:
        prediction_text += f"### {alerts[0].get("event")}\n"
        prediction_text += f"{alerts[0].get("description")}\n"

    if will_it_rain:
        if rain_start == 0:
            prediction_text += "It's raining"
        else:
            prediction_text += f"It's going to rain in {rain_start} minutes"
    else:
        prediction_text += "It will not rain in the following hour"

    prediction_text += "\n\n"

    prediction_text += f"Humidity: {c_humidity}%\n"
    prediction_text += f"Wind speed: {c_windspeed} m/s\n"
    prediction_text += f"Cloudiness:  {c_clouds}%\n"
    prediction_text += f"Visibility: {c_visibility} meters\n"
    prediction_text += f"UV index {c_uvindex}\n"
    prediction_text += f"Sunrise at {datetime.fromtimestamp(sunrise).time()} and sunset at {datetime.fromtimestamp(sunset).time()}\n"
    prediction_text += "\n\n"

    hourly = data.get("hourly", None)[:24]
    prediction_text += generate_hourly(hourly)

    send_to_discord(f"Weather forecast for {time}", prediction_text)

def send_to_discord(title, description):
    WEEBHOOK_URL = get_secret(DISCORD_WEBHOOK_URL_PATH)

    if not WEEBHOOK_URL:
        print("CRITICAL: Discord Webhook URL missing. Exiting.")
        return

    payload = {
        "username": "Weather Bot",
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": 0xADD8E6
            }
        ]
    }

    try:
        result = requests.post(WEEBHOOK_URL, json=payload)
        result.raise_for_status()
        print("Success! Payload delivered to Discord.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send to Discord: {e}")

def weather_send():
    weather_get_and_send()

##weather_get_and_send()