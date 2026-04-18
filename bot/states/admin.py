from aiogram.fsm.state import State, StatesGroup


class AdminReplyState(StatesGroup):
    waiting_appeal_reply = State()
    waiting_question_reply = State()