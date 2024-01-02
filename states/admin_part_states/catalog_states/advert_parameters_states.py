from aiogram.fsm.state import StatesGroup, State


class AdminAdvertParametersStates(StatesGroup):
    review_process = State()