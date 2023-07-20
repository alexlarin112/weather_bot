from peewee import *
from bot import logger

db = SqliteDatabase('./database/weather.db')


class BaseModel(Model):
    class Meta:
        database = db


class WeatherData(BaseModel):
    class Meta:
        db_table = 'weather'

    lat = FloatField()
    lon = FloatField()
    weather = TextField()
    base = CharField(150)
    temp = FloatField()
    temp_feels_like = FloatField()
    temp_min = FloatField()
    temp_max = FloatField()
    pressure = IntegerField()
    humidity = IntegerField()
    sea_level = IntegerField(null=True)
    grnd_level = IntegerField(null=True)
    visibility = IntegerField()
    wind = TextField()
    clouds = TextField()
    dt = IntegerField()
    sys = TextField()
    timezone = IntegerField()
    weather_id = IntegerField()
    name = CharField(200)
    cod = IntegerField()


class UVData(BaseModel):
    class Meta:
        db_table = "uv"

    lat = FloatField()
    lon = FloatField()
    uv = FloatField()
    uv_time = CharField(200)
    uv_max = FloatField()
    uv_max_time = CharField(200)
    ozone = IntegerField()
    ozone_time = CharField(200)
    safe_exposure_time = TextField()
    sun_info = TextField()


def get_weather_or_none(lat: float, lon: float) -> [None, dict]:
    try:
        return WeatherData.get_or_none(WeatherData.lat == lat, WeatherData.lon == lon)
    except Exception as e:
        logger.info("get_weather_data не выполнен")


def add_weather_data(lat: float, lon: float, weather: str, base: str, temp: str, temp_feels_like: str, temp_min: str,
                     temp_max: str, pressure: str, humidity: str, sea_level: str, grnd_level: str, visibility: str,
                     wind: str, clouds: str, dt: str, sys: str, timezone: str, weather_id: str, name: str, cod: str
                     ) -> None:
    pressure = translate_pressure(pressure)
    try:
        WeatherData(lat=lat, lon=lon, weather=weather, base=base, temp=temp, temp_feels_like=temp_feels_like,
                    temp_min=temp_min, temp_max=temp_max, pressure=pressure, humidity=humidity,
                    sea_level=sea_level, grnd_level=grnd_level, visibility=visibility, wind=wind, clouds=clouds,
                    dt=dt, sys=sys, timezone=timezone, weather_id=weather_id, name=name, cod=cod).save()
    except Exception as e:
        logger.info("add_weather_data не выполнен", e)


def update_weather_data(lat: float, lon: float, weather: str, base: str, temp: str, temp_feels_like: str, temp_min: str,
                        temp_max: str, pressure: str, humidity: str, sea_level: str, grnd_level: str, visibility: str,
                        wind: str, clouds: str, dt: str, sys: str, timezone: str, weather_id: str, name: str, cod: str
                        ) -> None:
    updated_data = {
        WeatherData.weather: weather,
        WeatherData.base: base,
        WeatherData.temp: temp,
        WeatherData.temp_feels_like: temp_feels_like,
        WeatherData.temp_min: temp_min,
        WeatherData.temp_max: temp_max,
        WeatherData.pressure: translate_pressure(pressure),
        WeatherData.humidity: humidity,
        WeatherData.sea_level: sea_level,
        WeatherData.grnd_level: grnd_level,
        WeatherData.visibility: visibility,
        WeatherData.wind: wind,
        WeatherData.clouds: clouds,
        WeatherData.dt: dt,
        WeatherData.timezone: timezone,
                  }
    try:
        WeatherData.update(updated_data).where(WeatherData.lat == lat, WeatherData.lon == lon).execute()
    except Exception as e:
        logger.info("update_weather_data не выполнен")


def get_uv_or_none(lat: float, lon: float) -> [None, dict]:
    try:
        return UVData.get_or_none(UVData.lat == lat, UVData.lon == lon)
    except Exception as e:
        logger.info("get_uv_data не выполнен", e)


def add_uv_data(lat: float, lon: float, uv: float, uv_time: str, uv_max: float,
                uv_max_time: str, ozone: int, ozone_time: str, safe_exposure_time: str, sun_info: str) -> None:
    try:
        UVData(lat=lat, lon=lon, uv=uv, uv_time=uv_time, uv_max = uv_max, uv_max_time=uv_max_time, ozone=ozone,
               ozone_time=ozone_time, safe_exposure_time=safe_exposure_time, sun_info=sun_info).save()
    except Exception as e:
        logger.info("add_uv_data не выполнен", e)


def update_uv_data(lat: float, lon: float, uv: float, uv_time: str, uv_max: float,
                   uv_max_time: str, ozone: int, ozone_time: str, safe_exposure_time: str, sun_info: str) -> None:
    updated_data = {
        UVData.uv: uv,
        UVData.uv_time: uv_time,
        UVData.uv_max: uv_max,
        UVData.uv_max_time: uv_max_time,
        UVData.ozone: ozone,
        UVData.ozone_time: ozone_time,
        UVData.safe_exposure_time: safe_exposure_time,
        UVData.sun_info: sun_info
    }
    try:
        UVData.update(updated_data).where(UVData.lat == lat, UVData.lon == lon).execute()
    except Exception as e:
        logger.info("update_uv_data не выполнен")


def parse_weather_data(data: dict) -> tuple[str, str, str, str, str, str, str, str,
                                            str, str, str, str, str, str, str, str, str, str, str]:
    weather = data.get('weather')
    base = data.get('base')
    temp = data['main'].get('temp')
    temp_feels_like = data['main'].get('feels_like')
    temp_min = data['main'].get('temp_min')
    temp_max = data['main'].get('temp_max')
    pressure = data['main'].get('pressure')
    humidity = data['main'].get('humidity')
    sea_level = data['main'].get('sea_level')
    grnd_level = data['main'].get('grnd_level')
    visibility = data.get('visibility')
    wind = data.get('wind')
    clouds = data.get('clouds')
    dt = data.get('dt')
    sys = data.get('sys')
    timezone = data.get('timezone')
    weather_id = data.get('id')
    name = data.get('name')
    cod = data.get('cod')

    return weather, base, temp, temp_feels_like, temp_min, temp_max, pressure, humidity, sea_level, grnd_level,\
           visibility, wind, clouds, dt, sys, timezone, weather_id, name, cod


def parse_uv_data(data: dict) -> tuple[str, str, str, str, str, str, str, str]:
    uv = round(data['result']['uv'], 1)
    uv_time = data['result']['uv_time'][:-5]
    uv_max = round(data['result']['uv_max'], 1)
    uv_max_time = data['result']['uv_max_time'][:-5]
    ozone = data['result']['ozone']
    ozone_time = data['result']['ozone_time'][:-5]
    safe_exposure_time = data['result']['safe_exposure_time']
    sun_info = data['result']['sun_info']

    return uv, uv_time, uv_max, uv_max_time, ozone, ozone_time, safe_exposure_time, sun_info


def translate_pressure(pressure: str) -> int:
    return int(int(pressure) / 1.333)


db.create_tables([WeatherData, UVData])
