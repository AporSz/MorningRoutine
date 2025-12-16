from datetime import datetime

def icons(icon_id):
    if icon_id == "01d":
        return ":sun:"
    if icon_id == "01n":
        return ":sun:"
    if icon_id == "02d":
        return ":white_sun_small_cloud:"
    if icon_id == "02n":
        return ":white_sun_small_cloud:"

    return ":smile:"

def generate_hourly(hourly):
    prediction_text = ""
    for item in hourly:
        prediction_text += f"- **{datetime.fromtimestamp(item.get("dt", None)).time().hour}**: {item.get("weather", None)[0].get("description", None)}; temp: **{item.get("temp", None)}°C** feels like {item.get("feels_like", None)}°C\n"

    return prediction_text