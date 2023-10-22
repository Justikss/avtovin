import importlib
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from states.hybrid_choose_states import HybridChooseStates
from database.data_requests.commodity_requests import CommodityRequester
from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import cache_state



async def choose_complectation_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    print('pre-tarue')
    await cache_state(callback=callback, state=state)

    memory_storage = await state.get_data()
    if first_call:
        user_answer = callback.data.split(':')[1]  # Второе слово - ключевое к значению бд
        await state.update_data(cars_engine_type=user_answer)
    else:
        user_answer = memory_storage['cars_engine_type']

    models_range = CommodityRequester.get_for_request(state=memory_storage['cars_state'],
                                                      brand=memory_storage['cars_brand'],
                                                      model=memory_storage['cars_model'],
                                                      engine_type=user_answer)

    button_texts = {car.complectation for car in models_range}
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='choose_complectation', button_texts=button_texts,
                                     callback_sign='cars_complectation:', lexicon_cache=False)

    await state.set_state(HybridChooseStates.config_output)
