from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.db.models import create_appeal
from bot.keyboards.inline import (
    appeal_categories_keyboard,
    anonymous_choice_keyboard,
    back_to_menu_keyboard,
    admin_appeal_reply_keyboard,
)
from bot.states.appeal import AppealState

router = Router()

ADMIN_IDS = [907403325, 5500054763]

CATEGORY_MAP = {
    "appeal_cat_oq_uv": "O‘quv jarayoni",
    "appeal_cat_ijtimoiy": "Ijtimoiy hayot",
    "appeal_cat_sharoit": "Sharoitlar",
    "appeal_cat_axborot": "Axborot yetishmasligi",
}


@router.callback_query(F.data == "menu_appeal")
async def start_appeal(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppealState.choosing_category)
    await callback.message.edit_text(
        "Murojaat turini tanlang:",
        reply_markup=appeal_categories_keyboard()
    )
    await callback.answer()


@router.callback_query(AppealState.choosing_category, F.data.startswith("appeal_cat_"))
async def choose_category(callback: CallbackQuery, state: FSMContext):
    category = CATEGORY_MAP.get(callback.data, "Boshqa")
    await state.update_data(category=category)
    await state.set_state(AppealState.writing_message)

    await callback.message.edit_text(
        f"Tanlandi: <b>{category}</b>\n\nEndi murojaatingizni yozing:"
    )
    await callback.answer()


@router.message(AppealState.writing_message)
async def write_appeal_message(message: Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    await state.set_state(AppealState.choosing_anonymous)

    await message.answer(
        "Murojaat anonim yuborilsinmi?",
        reply_markup=anonymous_choice_keyboard()
    )


@router.callback_query(AppealState.choosing_anonymous, F.data.in_(["appeal_anonymous_yes", "appeal_anonymous_no"]))
async def finish_appeal(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    is_anonymous = callback.data == "appeal_anonymous_yes"

    appeal_id = create_appeal(
        user_id=callback.from_user.id,
        full_name=callback.from_user.full_name,
        username=callback.from_user.username,
        category=data["category"],
        message=data["message_text"],
        is_anonymous=is_anonymous,
    )

    sender_info = "Anonim" if is_anonymous else (
        f"{callback.from_user.full_name} (@{callback.from_user.username})"
        if callback.from_user.username
        else callback.from_user.full_name
    )

    admin_text = (
        f"📥 <b>Yangi murojaat</b>\n\n"
        f"🆔 ID: <code>{appeal_id}</code>\n"
        f"👤 Yuboruvchi: {sender_info}\n"
        f"📂 Kategoriya: {data['category']}\n"
        f"📝 Matn:\n{data['message_text']}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await callback.bot.send_message(
                admin_id,
                admin_text,
                reply_markup=admin_appeal_reply_keyboard(appeal_id)
            )
        except Exception:
            pass

    await callback.message.edit_text(
        "✅ Murojaatingiz qabul qilindi. Admin ko‘rib chiqadi.",
        reply_markup=back_to_menu_keyboard()
    )
    await state.clear()
    await callback.answer()