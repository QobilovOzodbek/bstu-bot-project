from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import back_to_menu_keyboard
from bot.services.api_client import api_client

router = Router()


def format_news_items(items: list[dict]) -> str:
    if not items:
        return "Hozircha yangiliklar topilmadi."

    lines = ["📢 So'nggi yangiliklar:\n"]

    for idx, item in enumerate(items[:5], start=1):
        title = item.get("title", "Sarlavha yo'q")
        summary = item.get("summary", "") or "Qisqa matn mavjud emas."
        url = item.get("url", "")

        lines.append(
            f"{idx}. <b>{title}</b>\n"
            f"{summary}\n"
            f"<a href=\"{url}\">Batafsil</a>\n"
        )

    return "\n".join(lines)


@router.callback_query(F.data == "menu_news")
async def news_handler(callback: CallbackQuery):
    try:
        items = await api_client.get_news()
        text = format_news_items(items)

        await callback.message.edit_text(
            text,
            reply_markup=back_to_menu_keyboard(),
            disable_web_page_preview=True,
        )
    except Exception as e:
        await callback.message.edit_text(
            f"Yangiliklarni olishda xatolik yuz berdi:\n<code>{str(e)}</code>",
            reply_markup=back_to_menu_keyboard(),
            disable_web_page_preview=True,
        )

    await callback.answer()