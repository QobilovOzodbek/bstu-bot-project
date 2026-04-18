from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import back_to_menu_keyboard
from bot.services.api_client import api_client

router = Router()


def format_links(items: list[dict]) -> str:
    if not items:
        return "Tezkor havolalar topilmadi."

    lines = ["🔗 Tezkor havolalar:\n"]

    for item in items:
        lines.append(f"• <a href=\"{item.get('url', '')}\">{item.get('title', 'Link')}</a>")

    return "\n".join(lines)


@router.callback_query(F.data == "menu_links")
async def links_handler(callback: CallbackQuery):
    try:
        items = await api_client.get_quick_links()
        text = format_links(items)
        await callback.message.edit_text(
            text,
            reply_markup=back_to_menu_keyboard(),
            disable_web_page_preview=True,
        )
    except Exception as e:
        await callback.message.edit_text(
            f"Havolalarni olishda xatolik:\n<code>{str(e)}</code>",
            reply_markup=back_to_menu_keyboard(),
        )

    await callback.answer()