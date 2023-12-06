from aiogram.fsm.state import StatesGroup, State


class HybridChooseStates(StatesGroup):
    select_engine_type = State()
    select_brand = State()
    select_model = State()
    select_complectation = State()
    select_color = State()
    config_output = State()
