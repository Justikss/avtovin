from aiogram.fsm.state import StatesGroup, State


class HybridChooseStates(StatesGroup):
    select_brand = State()
    select_model = State()
    select_engine_type = State()
    config_output = State()
