from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import back_to_menu_keyboard
from bot.services.api_client import api_client

router = Router()


def format_leadership(items: list[dict]) -> str:
    if not items:
        return "Rahbariyat ma'lumotlari topilmadi."

    lines = ["🏛 Universitet rahbariyati:\n"]

    for item in items:
        lines.append(
            f"<b>{item.get('position', '')}</b>\n"
            f"👤 {item.get('full_name', 'Noma’lum')}\n"
            f"🕒 {item.get('reception_time', 'Ko‘rsatilmagan')}\n"
            f"📞 {item.get('phone', 'Ko‘rsatilmagan')}\n"
            f"✉️ {item.get('email', 'Ko‘rsatilmagan')}\n"
            f"<a href=\"{item.get('url', '')}\">Batafsil</a>\n"
        )

    return "\n".join(lines)


@router.callback_query(F.data == "menu_leadership")
async def leadership_handler(callback: CallbackQuery):
    try:
        items = await api_client.get_leadership()
        text = format_leadership(items)
        await callback.message.edit_text(
            text,
            reply_markup=back_to_menu_keyboard(),
            disable_web_page_preview=True,
        )
    except Exception as e:
        await callback.message.edit_text(
            f"Rahbariyat ma'lumotlarini olishda xatolik:\n<code>{str(e)}</code>",
            reply_markup=back_to_menu_keyboard(),
        )

    await callback.answer()