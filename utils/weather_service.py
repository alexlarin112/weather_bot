from typing import Callable
import requests
from time import time
import ast

import bot
from config_data.config import load_config, Config
from utils.time_service import get_local_time, get_unix_time, get_local_time_date
import database.database


config: Config = load_config()


def get_weather(lat, lon) -> tuple[str, str, str, str, int, str, str, str]:
    weather = database.database.get_weather_or_none(lat, lon)
    if weather is None:
        return request_weather_data(lat, lon, func=database.database.add_weather_data)
    elif weather.dt + 600 < time():
        return request_weather_data(lat, lon, func=database.database.update_weather_data)

    general_weather_info = ast.literal_eval(weather.weather)[0]

    return weather.temp, weather.pressure, weather.humidity, general_weather_info['description'], weather.timezone,\
           weather.name, get_local_time_date(weather.dt, weather.timezone), general_weather_info['icon']


def get_uv_index(lat: float, lon: float, timezone: int) -> tuple[str, str, str, str]:
    uv_data = database.database.get_uv_or_none(lat, lon)
    if uv_data:
        local_unix_time = get_unix_time(uv_data.uv_time) + int(timezone)
    if uv_data is None:
        return request_uv_data(lat, lon, timezone, func=database.database.add_uv_data)
    elif local_unix_time + 7200 < time():
        return request_uv_data(lat, lon, timezone, func=database.database.update_uv_data)

    # перевод в местое время пользователя
    uv_local_time = get_local_time(uv_data.uv_time, timezone)
    uv_local_max_time = get_local_time(uv_data.uv_max_time, timezone)

    return uv_data.uv, uv_local_time, uv_data.uv_max, uv_local_max_time


def request_uv_data(lat: float, lon: float, timezone: int, func) -> tuple[str, str, str, str]:
    URL = "https://api.openuv.io/api/v1/uv"

    data = {
        "lat": lat,
        "lng": lon,
        "alt": "100",
        "dt": ""
    }
    headers = {
        "x-access-token": config.weather.uv_index_api,
        "Content-Type": "application/json"
    }
    try:
        r = requests.get(URL, data, headers=headers).json()

        func(lat, lon, *database.database.parse_uv_data(r))   # add_uv_data or update_uv_data
        bot.logger.info("Request uv выполнен")

        # Передаем данные из реквеста, чтобы не делать доп. запрос к БД
        uv = round(r['result']['uv'], 1)
        uv_max = round(r['result']['uv_max'], 1)

        # перевод в местное время пользователя
        uv_local_time = get_local_time(r['result']['uv_time'][:-5], timezone)
        uv_local_max_time = get_local_time(r['result']['uv_max_time'][:-5], timezone)

        return uv, uv_local_time, uv_max, uv_local_max_time

    except KeyError as e:
        bot.logger.exception(e)
        return '-', '-', '-', '-'
    except Exception as e:
        bot.logger.exception(e)
        return '-', '-', '-', '-'


def request_weather_data(lat: float, lon: float,
                         func: Callable,
                         exclude="") -> tuple[str, [str, int], str, str, [str, int], str, str, str]:
    URL = "https://api.openweathermap.org/data/2.5/weather"
    data = {
        "lat": lat,
        "lon": lon,
        "exclude": exclude,
        'units': 'metric',
        "appid": config.weather.weather_api,
        'lang': 'ru',
    }

    try:
        r = requests.get(URL, data).json()
        bot.logger.info("Request weather выполнен")
        # database.add_weather_data or database.update_weather_data
        func(lat, lon, *database.database.parse_weather_data(r))

        # Передаем данные из реквеста, что не делать доп. запрос к БД
        temperature = r['main']['temp']
        timezone = r['timezone']
        pressure = database.database.translate_pressure(r['main']['pressure'])
        humidity = r['main']['humidity']
        description = r['weather'][0]['description']
        city_name = r['name']
        date = get_local_time_date(r['dt'], r['timezone'])
        icon = r['weather'][0]['icon']
        return temperature, pressure, humidity, description, timezone, city_name, date, icon
    except KeyError as e:
        bot.logger.exception(e)
        return '-', '-', '-', '-', '-', '-', '-', '-'
    except Exception as e:
        bot.logger.exception(e)
        return '-', '-', '-', '-', '-', '-', '-', '-'



