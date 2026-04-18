from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import main_menu_keyboard

router = Router()


@router.callback_query(F.data == "back_main_menu")
async def back_main_menu_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Asosiy menyu:",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()