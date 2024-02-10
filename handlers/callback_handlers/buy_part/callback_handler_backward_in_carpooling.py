import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.state_handlers.choose_car_for_buy import hybrid_handlers, second_hand_car_handlers
from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import search_auto_callback_handler


async def backward_in_carpooling_handler(callback: CallbackQuery, state: FSMContext):
    '''Кнопка "Назад" во время подбора автомобиля'''
    media_group_delete_module = importlib.import_module('utils.chat_cleaner.media_group_messages')
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

    await media_group_delete_module.delete_media_groups(request=callback)
    ic(await state.get_state())
    user_id = str(callback.from_user.id)
    redis_key = user_id + ':state_history_stack'
    states_stack = await redis_module.redis_data.get_data(key=redis_key, use_json=True)
    if states_stack:
        states_stack.pop()
        if len(states_stack) < 1:
            last_state = None
        else:
            last_state = states_stack[-1]
    else:
        last_state = None
    ic(last_state)
    await redis_module.redis_data.set_data(key=redis_key, value=states_stack)
    await state.set_state(last_state)
    if last_state is None:
        await search_auto_callback_handler(callback, state)
    if last_state == 'HybridChooseStates:select_engine_type':
        await hybrid_handlers.choose_engine_type_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'HybridChooseStates:select_brand':
        await hybrid_handlers.choose_brand_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'HybridChooseStates:select_model':
        await hybrid_handlers.choose_model_handler(callback=callback, state=state, first_call=False)
    elif last_state in ('HybridChooseStates:config_output', 'CheckActiveOffersStates:show_from_search_config'):
        memory_storage = await state.get_data()
        ic(memory_storage['cars_class'])
        if str(memory_storage['cars_class']) == '2':
            await second_hand_car_handlers.choose_year_of_release_handler(callback=callback, state=state, first_call=False)
        else:
            await hybrid_handlers.choose_complectation_handler(callback=callback, state=state, first_call=False)

    elif last_state == 'SecondHandChooseStates:select_year':
        await second_hand_car_handlers.choose_year_of_release_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'SecondHandChooseStates:select_mileage':
        await second_hand_car_handlers.choose_mileage_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'HybridChooseStates:select_color':
        await hybrid_handlers.choose_color_handler(callback=callback, state=state, first_call=False)
    elif last_state == 'HybridChooseStates:select_complectation':
        await hybrid_handlers.choose_complectation_handler(callback=callback, state=state, first_call=False)

    await callback.answer()
