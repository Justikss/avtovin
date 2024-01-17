from aiogram.fsm.state import StatesGroup, State


class TechSupportStates(StatesGroup):
    review = State()
    add_new = State()
    delete_exists = State()
    rewrite_exists = State()