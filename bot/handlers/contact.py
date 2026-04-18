from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import back_to_menu_keyboard
from bot.services.api_client import api_client

router = Router()


@router.callback_query(F.data == "menu_contact")
async def contact_handler(callback: CallbackQuery):
    try:
        item = await api_client.get_contact_info()
        text = (
            "📞 Universitet kontaktlari:\n\n"
            f"📍 <b>Manzil:</b> {item.get('address', 'Ko‘rsatilmagan')}\n"
            f"✉️ <b>Email:</b> {item.get('email', 'Ko‘rsatilmagan')}\n"
            f"📱 <b>Telefon:</b> {item.get('phone', 'Ko‘rsatilmagan')}"
        )
        await callback.message.edit_text(
            text,
            reply_markup=back_to_menu_keyboard(),
            disable_web_page_preview=True,
        )
    except Exception as e:
        await callback.message.edit_text(
            f"Kontaktlarni olishda xatolik:\n<code>{str(e)}</code>",
            reply_markup=back_to_menu_keyboard(),
        )

    await callback.answer()