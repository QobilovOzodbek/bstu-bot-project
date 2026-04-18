from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import back_to_menu_keyboard
from bot.services.api_client import api_client

router = Router()


def format_clubs(items: list[dict]) -> str:
    if not items:
        return "Hozircha to‘garaklar bo‘yicha ma’lumot topilmadi."

    lines = ["🎯 <b>To‘garaklar</b>\n"]

    for idx, item in enumerate(items, start=1):
        lines.append(
            f"{idx}. <b>{item.get('title', '')}</b>\n"
            f"📂 {item.get('category', 'Boshqa')}\n"
            f"📝 {item.get('description', '')}\n"
            f"🔗 <a href=\"{item.get('url', '')}\">Manba</a>\n"
        )

    return "\n".join(lines)


@router.callback_query(F.data == "menu_clubs")
async def clubs_handler(callback: CallbackQuery):
    try:
        items = await api_client.get_clubs()
        text = format_clubs(items)

        await callback.message.edit_text(
            text,
            reply_markup=back_to_menu_keyboard(),
            disable_web_page_preview=True,
        )
    except Exception as e:
        await callback.message.edit_text(
            f"To‘garaklarni olishda xatolik:\n<code>{str(e)}</code>",
            reply_markup=back_to_menu_keyboard(),
        )

    await callback.answer()