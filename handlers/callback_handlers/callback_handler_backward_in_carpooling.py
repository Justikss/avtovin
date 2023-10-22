import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.state_handlers.choose_car_for_buy import hybrid_handlers, second_hand_car_handlers, new_car_handlers
from handlers.state_handlers.choose_car_for_buy.new_car_handlers import choose_complectation_handler
from handlers.state_handlers.choose_car_for_buy.second_hand_car_handlers import choose_color_handler


async def backward_in_carpooling_handler(callback: CallbackQuery, state: FSMContext):
    '''Кнопка "Назад" в овремя подбора автомобиля'''
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    print('in backw')
    user_id = str(callback.from_user.id)
    redis_key = user_id + ':state_history_stack'
    states_stack = await redis_module.redis_data.get_data(key=redis_key, use_json=True)

    states_stack.pop()
    last_state = states_stack[-1]
    await redis_module.redis_data.set_data(key=redis_key, value=states_stack)
    await state.set_state(last_state)
    if last_state == 'HybridChooseStates:select_brand':
        await hybrid_handlers.choose_brand_handler(callback=callback, state=state)
    elif last_state == 'HybridChooseStates:select_model':
        await hybrid_handlers.choose_model_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'HybridChooseStates:select_engine_type':
        await hybrid_handlers.choose_engine_type_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'HybridChooseStates:config_output':
        print('may')
        memory_storage = await state.get_data()
        if memory_storage['cars_class'] == 'Б/У':
            await choose_color_handler(callback=callback, state=state, first_call=False)
        elif memory_storage['cars_class'] == 'Новая':
            await choose_complectation_handler(callback=callback, state=state, first_call=False)

    elif last_state == 'SecondHandChooseStates:select_year':
        await second_hand_car_handlers.choose_year_of_release_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'SecondHandChooseStates:select_mileage':
        await second_hand_car_handlers.choose_mileage_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'SecondHandChooseStates:select_color':
        await second_hand_car_handlers.choose_color_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'NewCarChooseStates:select_complectation':
        await new_car_handlers.choose_complectation_handler(callback=callback, state=state, first_call=False)

    await callback.answer()
