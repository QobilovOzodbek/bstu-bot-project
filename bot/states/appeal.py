from aiogram.fsm.state import State, StatesGroup


class AppealState(StatesGroup):
    choosing_category = State()
    writing_message = State()
    choosing_anonymous = State()