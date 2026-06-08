from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from app.db.models import (
    get_appeal_by_id,
    get_question_by_id,
    reply_to_appeal,
    reply_to_question,
    get_statistics,
)
from bot.states.admin import AdminReplyState
from bot.keyboards.inline import admin_panel_keyboard
router = Router()

ADMIN_IDS = [907403325, 5500054763, 903543672]


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.callback_query(F.data.startswith("admin_reply_appeal_"))
async def admin_reply_appeal_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Siz admin emassiz", show_alert=True)
        return

    appeal_id = int(callback.data.split("_")[-1])
    await state.set_state(AdminReplyState.waiting_appeal_reply)
    await state.update_data(appeal_id=appeal_id)

    await callback.message.answer(
        f"Murojaat ID <code>{appeal_id}</code> uchun javob matnini yuboring:"
    )
    await callback.answer()


@router.message(AdminReplyState.waiting_appeal_reply)
async def admin_reply_appeal_finish(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    appeal_id = data["appeal_id"]
    reply_text = message.text

    appeal = get_appeal_by_id(appeal_id)
    if not appeal:
        await message.answer("Murojaat topilmadi.")
        await state.clear()
        return

    reply_to_appeal(appeal_id, reply_text)

    try:
        await message.bot.send_message(
            appeal["user_id"],
            f"📩 <b>Murojaatingizga javob keldi</b>\n\n"
            f"🆔 ID: <code>{appeal_id}</code>\n"
            f"💬 Javob:\n{reply_text}"
        )
    except Exception:
        pass

    await message.answer("✅ Javob foydalanuvchiga yuborildi.")
    await state.clear()


@router.callback_query(F.data.startswith("admin_reply_question_"))
async def admin_reply_question_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Siz admin emassiz", show_alert=True)
        return

    question_id = int(callback.data.split("_")[-1])
    await state.set_state(AdminReplyState.waiting_question_reply)
    await state.update_data(question_id=question_id)

    await callback.message.answer(
        f"Savol ID <code>{question_id}</code> uchun javob matnini yuboring:"
    )
    await callback.answer()


@router.message(AdminReplyState.waiting_question_reply)
async def admin_reply_question_finish(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    question_id = data["question_id"]
    reply_text = message.text

    question = get_question_by_id(question_id)
    if not question:
        await message.answer("Savol topilmadi.")
        await state.clear()
        return

    reply_to_question(question_id, reply_text)

    try:
        await message.bot.send_message(
            question["user_id"],
            f"📩 <b>Savolingizga javob keldi</b>\n\n"
            f"🆔 ID: <code>{question_id}</code>\n"
            f"💬 Javob:\n{reply_text}"
        )
    except Exception:
        pass

    await message.answer("✅ Javob foydalanuvchiga yuborildi.")
    await state.clear()
@router.message(Command("admin"))
async def show_admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return # Admin bo'lmasa hech narsa qaytarmaydi
    
    await message.answer(
        "👨‍💻 <b>Admin paneliga xush kelibsiz!</b>\n\nQuyidagi menyudan kerakli bo'limni tanlang:",
        reply_markup=admin_panel_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "admin_statistics")
async def show_statistics_handler(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Siz admin emassiz!", show_alert=True)
        return

    stats = get_statistics()
    
    text = (
        "📊 <b>Botning umumiy statistikasi</b>\n\n"
        "📝 <b>Murojaatlar:</b>\n"
        f"▫️ Jami: <b>{stats['appeals']['total']}</b> ta\n"
        f"▫️ Yangi (kutilmoqda): <b>{stats['appeals']['new']}</b> ta\n"
        f"▫️ Javob berilgan: <b>{stats['appeals']['answered']}</b> ta\n\n"
        "❓ <b>Savollar:</b>\n"
        f"▫️ Jami: <b>{stats['questions']['total']}</b> ta\n"
        f"▫️ Yangi (kutilmoqda): <b>{stats['questions']['new']}</b> ta\n"
        f"▫️ Javob berilgan: <b>{stats['questions']['answered']}</b> ta\n"
    )
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=admin_panel_keyboard())
    await callback.answer()