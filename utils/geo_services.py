import requests
from config_data.config import load_config, Config
import bot

config: Config = load_config()


def get_city_coord(city: str) -> dict:
    URL = f"http://api.openweathermap.org/geo/1.0/direct"
    data = {"q": city,
            "limit": 5,
            "appid": config.weather.weather_api
            }

    try:
        r = requests.get(URL, data).json()

        city_data = dict()

        for city in r:
            city_name = city.get('local_names')
            if city_name:
                city_name = city_name.get('ru')
            else:
                city_name = city["name"]

            city_state = city.get("state")
            country = city.get("country")

            data = list()
            data.append(city_name)
            if city_state:
                data.append(city_state)
            if country:
                data.append(country)

            button_text = ", ".join(data)

            lat = round(float(city['lat']), 2)
            lon = round(float(city['lon']), 2)

            if len(f"{city_name}:{lat}:{lon}".encode('utf-8')) <= 64:
                button_callback = f"{city_name}:{lat}:{lon}"

                city_data[button_text] = button_callback

        return city_data

    except Exception as e:
        bot.logger.exception(e)
