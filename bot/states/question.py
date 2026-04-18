from aiogram.fsm.state import State, StatesGroup


class QuestionState(StatesGroup):
    writing_question = State()