import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.car_advert_requests import AdvertRequester
from database.tables.offers_history import ActiveOffers

from states.hybrid_choose_states import HybridChooseStates
from states.second_hand_choose_states import SecondHandChooseStates
from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import cache_state
from utils.Lexicon import ChooseColor, ChooseMileage, ChooseYearOfRelease
from utils.create_lexicon_part import create_lexicon_part


# ActiveOffers.create(seller=sellers[0], buyer=buyer[0], car=cars[0])
# ActiveOffers.create(seller=sellers[0], buyer=buyer[0], car=cars[3])
# ActiveOffers.create(seller=sellers[0], buyer=buyer[0], car=cars[1])
# ActiveOffers.create(seller=sellers[0], buyer=buyer[0], car=cars[2])


async def choose_color_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    print('pre-true')
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await cache_state(callback=callback, state=state)

    memory_storage = await state.get_data()
    if first_call:
        user_answer = int(callback.data.split('_')[-1])  # Второе слово - ключевое к значению бд
        await state.update_data(cars_complectation=user_answer)
    else:
        user_answer = memory_storage['cars_complectation']

    models_range = await AdvertRequester.get_advert_by(state_id=memory_storage['cars_state'],
                                                       brand_id=memory_storage['cars_brand'],
                                                       engine_type_id=memory_storage['cars_engine_type'],
                                                       model_id=memory_storage['cars_model'],
                                                       complectation_id=user_answer)


    button_texts = {car.color for car in models_range}
    lexicon_part = await create_lexicon_part(ChooseColor, button_texts)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part=lexicon_part, lexicon_cache=False)

    await callback.answer()
    await state.set_state(SecondHandChooseStates.select_mileage)


async def choose_mileage_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await cache_state(callback=callback, state=state)

    memory_storage = await state.get_data()
    if first_call:
        user_answer = int(callback.data.split('_')[-1])  # Второе слово - ключевое к значению бд
        await state.update_data(cars_color=user_answer)
    else:
        user_answer = memory_storage['cars_color']
    models_range = await AdvertRequester.get_advert_by(state_id=memory_storage['cars_state'],
                                                       brand_id=memory_storage['cars_brand'],
                                                       engine_type_id=memory_storage['cars_engine_type'],
                                                       model_id=memory_storage['cars_model'],
                                                       complectation_id=memory_storage['cars_complectation'],
                                                       color_id=user_answer)

    button_texts = {car.mileage for car in models_range}
    lexicon_part = await create_lexicon_part(ChooseMileage, button_texts)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part=lexicon_part, lexicon_cache=False)
    await callback.answer()
    await state.set_state(SecondHandChooseStates.select_year)



async def choose_year_of_release_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

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
    models_range = await AdvertRequester.get_advert_by(state_id=memory_storage['cars_state'],
                                                       brand_id=memory_storage['cars_brand'],
                                                       engine_type_id=memory_storage['cars_engine_type'],
                                                       model_id=memory_storage['cars_model'],
                                                       complectation_id=memory_storage['cars_complectation'],
                                                       color_id=memory_storage['cars_color'],
                                                       mileage_id=user_answer)

    button_texts = {car.year for car in models_range}
    lexicon_part = await create_lexicon_part(ChooseYearOfRelease, button_texts)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part=lexicon_part, lexicon_cache=False)
    await callback.answer()
    await state.set_state(HybridChooseStates.config_output)


