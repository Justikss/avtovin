from aiogram.fsm.state import StatesGroup, State


class NewCarChooseStates(StatesGroup):
    select_complectation = State()
