from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.inline import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "Assalomu alaykum.\n\n"
        "BSTU botiga xush kelibsiz.\n"
        "Kerakli bo'limni tanlang:"
    )
    await message.answer(text, reply_markup=main_menu_keyboard())