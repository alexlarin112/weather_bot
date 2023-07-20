from datetime import timedelta
from time import mktime, strptime, strftime, localtime, gmtime
import requests
from environs import Env
import json


# получение UNIX времени из формата дата + время
def get_unix_time(timestamp: str | int) -> float:
    struct_time = strptime(str(timestamp), '%Y-%m-%dT%H:%M:%S')
    unix_time = mktime(struct_time)
    return unix_time


# корректировка UTC даты в местное время в формат hh:mm
def get_local_time(timestamp: str | int, timezone: float | int) -> str:
    local_time = strftime('%H:%M', localtime(get_unix_time(timestamp) + float(timezone)))
    return local_time


# перевод местного времени пользователя в UTC
# для корректировки времени работы планировщика уведомлений из и в формат hh:mm
def get_utc_time(local_time: str, timezone: int | str) -> str:
    hours, minutes = local_time.split(':')
    utc_time = timedelta(hours=int(hours), minutes=int(minutes)) - timedelta(seconds=int(timezone))
    utc_time = str(utc_time)[:-3]

    return utc_time


def get_local_time_date(timestamp: str | int, timezone: float | int) -> str:
    local_time = strftime('%H:%M %d.%m', gmtime(int(timestamp) + int(timezone)))
    return local_time


def get_timezone_from_coord(lat, lon):
    env = Env()
    env.read_env()

    API_KEY = env('TIMEZONEDB_API_KEY')
    url = 'http://api.timezonedb.com/v2.1/get-time-zone'
    data = {
        'key': API_KEY,
        'format': 'json',
        'by': 'position',
        'lat': lat,
        'lng': lon

    }

    r = requests.get(url, data)

    print(json.dumps(r.json(), indent=2))
