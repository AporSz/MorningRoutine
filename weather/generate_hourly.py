from datetime import datetime

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