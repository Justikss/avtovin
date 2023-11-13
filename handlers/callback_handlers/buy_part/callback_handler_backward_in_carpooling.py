import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.state_handlers.choose_car_for_buy import hybrid_handlers, second_hand_car_handlers, new_car_handlers
from handlers.state_handlers.choose_car_for_buy.second_hand_car_handlers import choose_color_handler


async def backward_in_carpooling_handler(callback: CallbackQuery, state: FSMContext):
    '''Кнопка "Назад" во время подбора автомобиля'''
    media_group_delete_module = importlib.import_module('utils.chat_cleaner.media_group_messages')
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

    await media_group_delete_module.delete_media_groups(request=callback)

    print('in backw')
    user_id = str(callback.from_user.id)
    redis_key = user_id + ':state_history_stack'
    states_stack = await redis_module.redis_data.get_data(key=redis_key, use_json=True)

    states_stack.pop()
    last_state = states_stack[-1]
    print('last state', last_state)
    await redis_module.redis_data.set_data(key=redis_key, value=states_stack)
    await state.set_state(last_state)
    if last_state == 'HybridChooseStates:select_engine_type':
        await hybrid_handlers.choose_engine_type_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'HybridChooseStates:select_brand':
        await hybrid_handlers.choose_brand_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'HybridChooseStates:select_model':
        await hybrid_handlers.choose_model_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'HybridChooseStates:config_output':
        print('may', last_state)
        memory_storage = await state.get_data()
        if memory_storage['cars_class'] == 'Б/У':
            await second_hand_car_handlers.choose_year_of_release_handler(callback=callback, state=state, first_call=False)
        elif memory_storage['cars_class'] == 'Новая':
            await hybrid_handlers.choose_complectation_handler(callback=callback, state=state, first_call=False)

    elif last_state == 'SecondHandChooseStates:select_year':
        await second_hand_car_handlers.choose_year_of_release_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'SecondHandChooseStates:select_mileage':
        await second_hand_car_handlers.choose_mileage_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'SecondHandChooseStates:select_color':
        print('select_color')
        await second_hand_car_handlers.choose_color_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'HybridChooseStates:select_complectation':
        print('select_complect')
        await hybrid_handlers.choose_complectation_handler(callback=callback, state=state, first_call=False)

    await callback.answer()
