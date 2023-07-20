from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON, LEXICON_TIMER_INLINE_KB


def set_start_kb() -> ReplyKeyboardMarkup:
    coord_button = KeyboardButton(text=LEXICON["set_geo_button"], request_location=True)
    city_button = KeyboardButton(text=LEXICON['choose_city'])
    markup_request = ReplyKeyboardMarkup(keyboard=[[coord_button, city_button]], resize_keyboard=True)

    return markup_request


def set_basic_kb() -> ReplyKeyboardMarkup:
    coord_button = KeyboardButton(text=LEXICON["update_geo_button"], request_location=True)
    city_button = KeyboardButton(text=LEXICON['choose_city'])
    weather_button = KeyboardButton(text=LEXICON["weather_info_button"])
    timer_button = KeyboardButton(text=LEXICON['notification_button'])
    markup_request = ReplyKeyboardMarkup(keyboard=[[weather_button], [timer_button], [coord_button, city_button]],
                                         resize_keyboard=True)

    return markup_request


def set_notification_options_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = list()

    buttons.append(InlineKeyboardButton(text='Настроить время уведомления', callback_data='to_choose_timer'))
    buttons.append(InlineKeyboardButton(text='Отключить активные', callback_data='disable_notification'))
    buttons.append(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    kb_builder.row(*buttons, width=1)

    return kb_builder.as_markup()


def set_timer_inline_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = list()

    for value in LEXICON_TIMER_INLINE_KB:
        buttons.append(InlineKeyboardButton(text=value, callback_data=value))

    buttons.append(InlineKeyboardButton(text='Назад', callback_data='to_notification_menu'))
    kb_builder.row(*buttons, width=6)

    return kb_builder.as_markup()


def set_cities_inline_kb(cities) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = list()

    for city, callback in cities.items():
        buttons.append(InlineKeyboardButton(text=city, callback_data=callback))

    buttons.append(InlineKeyboardButton(text='Отмена', callback_data='Cancel'))
    kb_builder.row(*buttons, width=1)

    return kb_builder.as_markup()


def set_cancel_choose_city_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text='Отмена', callback_data='Cancel')]

    kb_builder.row(*buttons)

    return kb_builder.as_markup()
