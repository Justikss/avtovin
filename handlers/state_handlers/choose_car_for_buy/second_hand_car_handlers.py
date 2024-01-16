import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from states.second_hand_choose_states import SecondHandChooseStates
from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import cache_state, output_choose

config_module = importlib.import_module('config_data.config')
car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')

async def choose_mileage_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    await cache_state(callback=callback, state=state)

    memory_storage = await state.get_data()
    if first_call:
        user_answer = int(callback.data.split('_')[-1])  # Второе слово - ключевое к значению бд
        await state.update_data(cars_color=user_answer)
    else:
        user_answer = memory_storage['cars_color']
    models_range = await car_advert_requests_module.AdvertRequester.get_advert_by(state_id=memory_storage['cars_state'],
                                                       brand_id=memory_storage['cars_brand'],
                                                       engine_type_id=memory_storage['cars_engine_type'],
                                                       model_id=memory_storage['cars_model'],
                                                       complectation_id=memory_storage['cars_complectation'],
                                                       color_id=user_answer,
                                                       buyer_search_mode=callback.from_user.id)

    # button_texts = {car.mileage for car in models_range}
    lexicon_class = lexicon_module.ChooseMileage()
    await output_choose(callback, state, lexicon_class, models_range, config_module.car_configurations_in_keyboard_page)

    # lexicon_part = await create_lexicon_part(lexicon_class, models_range)
    # await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
    #                                                 lexicon_part=lexicon_part, lexicon_cache=False, dynamic_buttons=lexicon_class.dynamic_buttons)
    await callback.answer()
    await state.set_state(SecondHandChooseStates.select_year)



async def choose_year_of_release_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    choose_car_states_module = importlib.import_module('states.hybrid_choose_states')
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    await cache_state(callback=callback, state=state)

    if not first_call:
        delete_mode = True
    else:
        delete_mode = False

    memory_storage = await state.get_data()
    if first_call:
        user_answer = int(callback.data.split('_')[-1])  # Второе слово - ключевое к значению бд
        await state.update_data(cars_mileage=user_answer)
    else:
        user_answer = memory_storage['cars_mileage']
    models_range = await car_advert_requests_module.AdvertRequester.get_advert_by(state_id=memory_storage['cars_state'],
                                                       brand_id=memory_storage['cars_brand'],
                                                       engine_type_id=memory_storage['cars_engine_type'],
                                                       model_id=memory_storage['cars_model'],
                                                       complectation_id=memory_storage['cars_complectation'],
                                                       color_id=memory_storage['cars_color'],
                                                       mileage_id=user_answer,
                                                       buyer_search_mode=callback.from_user.id)

    # button_texts = {car.year for car in models_range}
    lexicon_class = lexicon_module.ChooseYearOfRelease()
    # lexicon_part = await create_lexicon_part(lexicon_class, models_range)
    await output_choose(callback, state, lexicon_class, models_range, config_module.car_configurations_in_keyboard_page)
    # await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
    #                                                 lexicon_part=lexicon_part, lexicon_cache=False, delete_mode=delete_mode,
    #                                                 dynamic_buttons=lexicon_class.dynamic_buttons)
    await callback.answer()
    await state.set_state(choose_car_states_module.HybridChooseStates.config_output)


