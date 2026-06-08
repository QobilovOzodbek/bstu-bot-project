from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📢 Yangiliklar", callback_data="menu_news"),
                InlineKeyboardButton(text="📣 E'lonlar", callback_data="menu_announcements"),
            ],
            [
                InlineKeyboardButton(text="🏛 Rahbariyat", callback_data="menu_leadership"),
            ],
            [
                InlineKeyboardButton(text="📞 Kontaktlar", callback_data="menu_contact"),
                InlineKeyboardButton(text="🔗 Havolalar", callback_data="menu_links"),
            ],
            [
                InlineKeyboardButton(text="🎯 To‘garaklar", callback_data="menu_clubs"),
            ],
            [
                InlineKeyboardButton(text="🗣 Murojaat qoldirish", callback_data="menu_appeal"),
            ],
            [
                InlineKeyboardButton(text="❓ Savol berish", callback_data="menu_question"),
            ],
        ]
    )


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_main_menu")]
        ]
    )


def appeal_categories_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📘 O‘quv jarayoni", callback_data="appeal_cat_oq_uv")],
            [InlineKeyboardButton(text="👥 Ijtimoiy hayot", callback_data="appeal_cat_ijtimoiy")],
            [InlineKeyboardButton(text="🏢 Sharoitlar", callback_data="appeal_cat_sharoit")],
            [InlineKeyboardButton(text="ℹ️ Axborot yetishmasligi", callback_data="appeal_cat_axborot")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_main_menu")],
        ]
    )


def anonymous_choice_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Ha, anonim", callback_data="appeal_anonymous_yes"),
                InlineKeyboardButton(text="❌ Yo‘q", callback_data="appeal_anonymous_no"),
            ]
        ]
    )


def admin_appeal_reply_keyboard(appeal_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Javob berish", callback_data=f"admin_reply_appeal_{appeal_id}")]
        ]
    )


def admin_question_reply_keyboard(question_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Javob berish", callback_data=f"admin_reply_question_{question_id}")]
        ]
    )

def admin_panel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_statistics")]
        ]
    )