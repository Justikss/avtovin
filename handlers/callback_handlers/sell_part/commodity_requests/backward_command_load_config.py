import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from states.load_commodity_states import LoadCommodityStates


# from handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers import input_state_to_load, \
#     input_engine_type_to_load, input_brand_to_load, input_model_to_load, input_complectation_to_load, \
#     input_color_to_load, input_price_to_load
# from handlers.state_handlers.seller_states_handler.load_new_car.second_hand_handlers import input_mileage_to_load, \
#     input_year_to_load


async def backward_in_boot_car(callback: CallbackQuery, state: FSMContext):
    memory_storage = await state.get_data()
    cached_states = memory_storage.get('boot_car_states_cache')
    ic()
    loader_module = importlib.import_module('loader')
    if cached_states:
        ic(cached_states)
        cached_states.pop()
        ic(cached_states)
        state_to_switch = cached_states[-1]
        await state.update_data(boot_car_states_cache=cached_states)

        if state_to_switch == 'LoadCommodityStates:input_to_load_state':
            current_state = LoadCommodityStates.input_to_load_price
            current_function = loader_module.load_new_car.hybrid_handlers.input_state_to_load
        elif state_to_switch == 'LoadCommodityStates:input_to_load_engine_type':
            current_state = LoadCommodityStates.input_to_load_engine_type
            current_function = loader_module.load_new_car.hybrid_handlers.input_engine_type_to_load
        elif state_to_switch == 'LoadCommodityStates:input_to_load_brand':
            current_state = LoadCommodityStates.input_to_load_brand
            current_function = loader_module.load_new_car.hybrid_handlers.input_brand_to_load
        elif state_to_switch == 'LoadCommodityStates:input_to_load_model':
            current_state = LoadCommodityStates.input_to_load_model
            current_function = loader_module.load_new_car.hybrid_handlers.input_model_to_load
        elif state_to_switch == 'LoadCommodityStates:input_to_load_complectation':
            current_state = LoadCommodityStates.input_to_load_complectation
            current_function = loader_module.load_new_car.hybrid_handlers.input_complectation_to_load
        elif state_to_switch == 'LoadCommodityStates:input_to_load_color':
            current_state = LoadCommodityStates.input_to_load_color
            current_function = loader_module.load_new_car.hybrid_handlers.input_color_to_load
        elif state_to_switch == 'LoadCommodityStates:input_to_load_price':
            current_state = LoadCommodityStates.input_to_load_price
            current_function = loader_module.load_new_car.hybrid_handlers.input_price_to_load

        elif state_to_switch == 'LoadCommodityStates:input_to_load_year':
            current_state = LoadCommodityStates.input_to_load_year
            current_function = loader_module.load_new_car.second_hand_handlers.input_year_to_load
        elif state_to_switch == 'LoadCommodityStates:input_to_load_mileage':
            current_state = LoadCommodityStates.input_to_load_mileage
            current_function = loader_module.load_new_car.second_hand_handlers.input_mileage_to_load

        else:
            current_state = None
            current_function = None

        if current_state:
            await state.set_state(current_state)

        if current_function:
            await current_function(callback, state)
