from aiogram.filters.state import State, StatesGroup


class FSMFillGeo(StatesGroup):
    fill_geo = State()      # пользователь прислал геолокацию


class FSMFillCity(StatesGroup):
    not_fill_city = State()
    get_city_kb = State()
    fill_city = State()