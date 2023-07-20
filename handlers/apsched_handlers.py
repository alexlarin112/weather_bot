from os.path import join
from aiogram import F
from aiogram import Bot, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Text, StateFilter
from apscheduler_di import ContextSchedulerDecorator
from aiogram.fsm.context import FSMContext

from keyboards.keyboard import set_timer_inline_kb, set_notification_options_kb
from lexicon.lexicon import LEXICON, LEXICON_TIMER_INLINE_KB
from utils.planing_message import create_delayed_notification, remove_delayed_notification, remove_all_delayed_notifications
from utils.weather_service import get_weather, get_uv_index
from utils.time_service import get_utc_time
from utils.image_draw.preparing_images import WeatherNowImage
from database.fsm import FSMFillGeo, FSMFillCity
from config_data.config import load_config


router: Router = Router()


#   хендлер срабатывает по нажатию на кнопку 'Уведомление'
@router.message(StateFilter(FSMFillGeo.fill_geo, FSMFillCity.fill_city), Text(text=LEXICON['notification_button']))
async def show_notification_options(message: Message) -> None:
    await message.answer(LEXICON["notification_options"], reply_markup=set_notification_options_kb())


#   хендлер срабатывает на callback для кнопки 'Настроить' в меню настройки уведомления
@router.callback_query(StateFilter(FSMFillGeo.fill_geo, FSMFillCity.fill_city), Text(text='to_choose_timer'))
async def open_notification_times(callback: CallbackQuery, bot: Bot) -> None:
    await bot.edit_message_text(text=LEXICON["choose_time"],
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=set_timer_inline_kb())


#   хендлер срабатывает на callback для кнопки 'Отключить активные' в меню настройки уведомления
@router.callback_query(StateFilter(FSMFillGeo.fill_geo, FSMFillCity.fill_city), Text(text='disable_notification'))
async def disable_notification(callback: CallbackQuery, bot: Bot, apscheduler: ContextSchedulerDecorator) -> None:
    remove_delayed_notification(callback.from_user.id, apscheduler)
    await bot.edit_message_text(text=LEXICON["disable_notification"],
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=None)


#   хендлер срабатывает на callback для кнопки 'Отмена' в меню настройки уведомления
@router.callback_query(StateFilter(FSMFillGeo.fill_geo, FSMFillCity.fill_city), Text(text='cancel'))
async def close_notification_menu(callback: CallbackQuery, bot: Bot) -> None:
    await bot.edit_message_text(text=LEXICON["cancel"],
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=None)


#   хендлер срабатывает на callback c любой кнопки для включения уведомления по таймеру
@router.callback_query(StateFilter(FSMFillGeo.fill_geo, FSMFillCity.fill_city), Text(text=LEXICON_TIMER_INLINE_KB))
async def choose_time_for_notification(callback: CallbackQuery, state: FSMContext, bot: Bot,
                                       apscheduler: ContextSchedulerDecorator) -> None:
    data = await state.get_data()
    lat = data['lat']
    lon = data['lon']
    timezone = data['timezone']
    utc_time = get_utc_time(callback.data, timezone)

    create_delayed_notification(send_delayed_weather_info, callback.from_user.id, lat, lon, utc_time, apscheduler)
    await bot.edit_message_text(text=LEXICON["enable_notification"].format(callback.data),
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=None)


#   хендлер срабатывает на callback для кнопки 'Назад' при выборе времени уведомления
@router.callback_query(StateFilter(FSMFillGeo.fill_geo, FSMFillCity.fill_city), Text(text='to_notification_menu'))
async def choose_notification_settings(callback: CallbackQuery, bot: Bot) -> None:
    await bot.edit_message_text(text=LEXICON['notification_options'],
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=set_notification_options_kb())


#   хендлер для админа для выставления уведомления через текст
@router.message(Text(contains=":"), F.from_user.id.in_(load_config().tg_bot.admin_ids))
async def admin_choose_time_for_notification(message: Message, state: FSMContext,
                                             apscheduler: ContextSchedulerDecorator) -> None:
    data = await state.get_data()
    lat = data['lat']
    lon = data['lon']
    timezone = data['timezone']
    utc_time = get_utc_time(message.text, timezone)

    create_delayed_notification(send_delayed_weather_info, message.from_user.id, lat, lon, utc_time, apscheduler)

    await message.answer(text=LEXICON["enable_notification"].format(message.text))


#   корутина для вызова планировщиком по таймеру
async def send_delayed_weather_info(user_id: str, lat: float, lon: float, bot: Bot) -> None:
    temp, pressure, humidity, description, timezone, city_name, date, icon = get_weather(lat, lon)
    uv, uv_time, uv_max, uv_max_time = get_uv_index(lat, lon, timezone)

    image = WeatherNowImage()
    image.create_weather_image(name=city_name, date=date, temperature=int(temp),
                               description=description, uv=uv, uv_time=uv_time, uv_max=uv_max, uv_max_time=uv_max_time,
                               filename=user_id, pressure=pressure, humidity=humidity, icon=icon
                               )

    path = join('.', 'media', f'{(str(user_id))}.png')
    photo = FSInputFile(path)
    await bot.send_photo(user_id, photo)
