from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.db.models import create_question
from bot.keyboards.inline import back_to_menu_keyboard, admin_question_reply_keyboard
from bot.states.question import QuestionState

router = Router()

ADMIN_IDS = [907403325, 5500054763]


@router.callback_query(F.data == "menu_question")
async def start_question(callback: CallbackQuery, state: FSMContext):
    await state.set_state(QuestionState.writing_question)
    await callback.message.edit_text(
        "Savolingizni yozing:"
    )
    await callback.answer()


@router.message(QuestionState.writing_question)
async def save_question(message: Message, state: FSMContext):
    question_id = create_question(
        user_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username,
        question=message.text,
    )

    sender_info = (
        f"{message.from_user.full_name} (@{message.from_user.username})"
        if message.from_user.username
        else message.from_user.full_name
    )

    admin_text = (
        f"❓ <b>Yangi savol</b>\n\n"
        f"🆔 ID: <code>{question_id}</code>\n"
        f"👤 Yuboruvchi: {sender_info}\n"
        f"📝 Savol:\n{message.text}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(
                admin_id,
                admin_text,
                reply_markup=admin_question_reply_keyboard(question_id)
            )
        except Exception:
            pass

    await message.answer(
        "✅ Savolingiz yuborildi. Admin tez orada javob beradi.",
        reply_markup=back_to_menu_keyboard()
    )
    await state.clear()