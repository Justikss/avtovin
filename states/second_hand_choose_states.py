from aiogram.fsm.state import StatesGroup, State


class SecondHandChooseStates(StatesGroup):
    select_year = State()
    select_mileage = State()
    select_color = State()
