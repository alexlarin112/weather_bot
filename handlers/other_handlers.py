from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from keyboards.keyboard import set_basic_kb


router: Router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message(Command(commands='about_uv_index'))
async def send_about_uv(message: Message) -> None:
    await message.answer(LEXICON['about_uv_index'])


@router.message(Command(commands='about_spf'))
async def send_about_spf(message: Message) -> None:
    await message.answer(LEXICON['about_spf'])


@router.message()
async def send_echo(message: Message) -> None:
    await message.answer(LEXICON['other_message'], reply_markup=set_basic_kb())

