from aiogram.fsm.state import StatesGroup, State


class LoadCommodityStates(StatesGroup):
    input_to_load_state = State()
    input_to_load_engine_type = State()
    input_to_load_brand = State()
    input_to_load_model = State()
    input_to_load_complectation = State()
    

    input_to_load_year = State()
    input_to_load_mileage = State()
    input_to_load_color = State()

    input_to_load_price = State()
    input_to_load_photo = State()
    photo_verification = State()
    load_config_output = State()