from aiogram.fsm.state import StatesGroup, State


class AdminAdvertParametersStates(StatesGroup):
    review_process = State()
    start_add_value_process = State()
    confirmation_add_value_process = State()
    start_delete_action = State()