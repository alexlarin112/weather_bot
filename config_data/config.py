from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Weather:
    weather_api: str      # Токен для запросов по api https://openweathermap.org/
    uv_index_api: str     # Токен для запросов по api https://www.openuv.io/


@dataclass
class Config:
    tg_bot: TgBot
    weather: Weather


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
                    token=env('BOT_TOKEN'),
                    admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                  weather=Weather(
                    weather_api=env("OPEN_WEATHER_API_KEY"),
                    uv_index_api=env("OPENUV_API_KEY")))


