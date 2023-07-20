from os.path import join
from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON
from database.fsm import FSMFillCity
from keyboards.keyboard import set_start_kb, set_basic_kb, set_cities_inline_kb, set_cancel_choose_city_kb
from utils.weather_service import get_weather, get_uv_index
from database.fsm import FSMFillGeo
from utils.image_draw.preparing_images import WeatherNowImage
from utils.geo_services import get_city_coord


router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    await message.answer(LEXICON[message.text], reply_markup=set_start_kb())


# Этот хэндлер будет срабатывать на команду "/help"
@router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет реагировать на отправку геопозиции пользователя по кнопке
@router.message(F.location)
async def get_coordinate(message: Message, state: FSMContext) -> None:
    print(type(message.location))
    location = dict(message.location)

    lat = round(location["latitude"], 2)
    lon = round(location["longitude"], 2)
    _, _, _, _, timezone, city, _, _ = get_weather(lat, lon)

    await state.update_data(lon=lon, lat=lat, city=city, timezone=timezone)
    await state.set_state(FSMFillGeo.fill_geo)
    await message.answer(LEXICON["got_geo"], reply_markup=set_basic_kb())


#   хендлер работает по кнопке 'Выбрать город'
@router.message(Text(text=LEXICON['choose_city']))
async def start_get_city(message: Message, state: FSMContext) -> None:
    await state.set_state(FSMFillCity.not_fill_city)
    await message.answer(text=LEXICON['write_city'], reply_markup=set_cancel_choose_city_kb())


#   хендлер работает по кнопке 'Отмена' при написании или выборе города
@router.callback_query(StateFilter(FSMFillCity.not_fill_city, FSMFillCity.get_city_kb), Text(text='Cancel'))
async def cancel_get_city(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await state.clear()
    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                text='Отмена', reply_markup=None)


#   хендлер работает на написание текста для поиска города
@router.message(StateFilter(FSMFillCity.not_fill_city))
async def get_city_kb(message: Message, state: FSMContext) -> None:
    cities = get_city_coord(message.text)
    if not cities:
        await state.clear()
        await message.answer(text=LEXICON['city_not_found'], reply_markup=set_start_kb())
    else:
        await state.set_state(FSMFillCity.get_city_kb)
        await message.answer(text=LEXICON['list_of_cities'], reply_markup=set_cities_inline_kb(cities))


#   хендлер работает на нажатие инлайн кнопки с названием города
@router.callback_query(StateFilter(FSMFillCity.get_city_kb))
async def get_city(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await state.set_state(FSMFillCity.fill_city)
    data = callback.data.split(":")
    city, lat, lon = data
    _, _, _, _, timezone, _, _, _ = get_weather(lat, lon)

    await state.update_data(lat=lat, lon=lon, city=city, timezone=timezone)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text=LEXICON["got_geo"], reply_markup=set_basic_kb())


# Хэндлер работает на кнопку 'Погода'
@router.message(StateFilter(FSMFillGeo.fill_geo, FSMFillCity.fill_city), Text(text=LEXICON['weather_info_button']))
async def send_weather_image(message: Message, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    lat, lon, city_name = data['lat'], data['lon'], data['city']

    temp, pressure, humidity, description, timezone, _, date, icon = get_weather(lat, lon)
    uv, uv_time, uv_max, uv_max_time = get_uv_index(lat, lon, timezone)

    image = WeatherNowImage()
    image.create_weather_image(name=city_name, date=date, temperature=int(temp),
                               description=description, uv=uv, uv_time=uv_time, uv_max=uv_max, uv_max_time=uv_max_time,
                               filename=message.from_user.id, pressure=pressure, humidity=humidity, icon=icon
                               )

    path = join('.', 'media', f'{(str(message.from_user.id))}.png')
    photo = FSInputFile(path)
    await bot.send_photo(message.from_user.id, photo)

