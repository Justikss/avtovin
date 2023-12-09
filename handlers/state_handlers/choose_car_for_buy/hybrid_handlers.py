import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.car_advert_requests import AdvertRequester

# from database.data_requests.offers_requests import CachedOrderRequests
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_cars_pagination_system.pagination_system_for_buyer import \
    BuyerCarsPagination
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_chosen_search_config import get_cars_data_pack
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.states_cacher import cache_state
from states.hybrid_choose_states import HybridChooseStates
from states.second_hand_choose_states import SecondHandChooseStates
from utils.create_lexicon_part import create_lexicon_part


async def choose_engine_type_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    await cache_state(callback=callback, state=state, first=True)

    redis_key = str(callback.from_user.id) + ':cars_type'
    cars_type = await message_editor.redis_data.get_data(redis_key)

    models_range = await AdvertRequester.get_advert_by(state_id=cars_type)
    if not models_range:
        return await message_editor.travel_editor.edit_message(request=callback, lexicon_key='cars_not_found', lexicon_cache=False)


    await state.update_data(cars_state=cars_type)

    await state.update_data(cars_class=cars_type)

    button_texts = {car.engine_type for car in models_range}
    lexicon_part = await create_lexicon_part(lexicon_module.ChooseEngineType, button_texts)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                     lexicon_part=lexicon_part, lexicon_cache=False, dynamic_buttons=1)

    await callback.answer()
    await state.set_state(HybridChooseStates.select_brand)



async def choose_brand_handler(callback: CallbackQuery, state: FSMContext, first_call: object = True) -> object:
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    await cache_state(callback=callback, state=state)

    memory_storage = await state.get_data()

    if first_call:
        user_answer = int(callback.data.split('_')[-1])  # Второе слово - ключевое к значению бд
        await state.update_data(cars_engine_type=user_answer)
        print(user_answer)
    else:
        user_answer = memory_storage['cars_engine_type']

    models_range = await AdvertRequester.get_advert_by(state_id=memory_storage['cars_state'],
                                                    engine_type_id=user_answer,
                                                    )

    button_texts = {car.complectation.model.brand for car in models_range}
    lexicon_class = lexicon_module.ChooseBrand()
    lexicon_part = await create_lexicon_part(lexicon_class, button_texts)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                     lexicon_part=lexicon_part, lexicon_cache=False, dynamic_buttons=lexicon_class.dynamic_buttons)


    '''Кэширование для кнопки НАЗАД'''
    # await backward_in_carpooling_controller(callback=callback, state=state)
    await callback.answer()
    await state.set_state(HybridChooseStates.select_model)


async def choose_model_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


    await cache_state(callback=callback, state=state)

    memory_storage = await state.get_data()
    commodity_state = memory_storage['cars_state']
    engine_type = memory_storage['cars_engine_type']

    if first_call:
        user_answer = int(callback.data.split('_')[-1]) #Второе слово - ключевое к значению бд
        brand = user_answer
        await state.update_data(cars_brand=brand)
    else:
        brand = memory_storage['cars_brand']


    models_range = await AdvertRequester.get_advert_by(state_id=commodity_state, brand_id=brand, engine_type_id=engine_type)

    button_texts = {car.complectation.model for car in models_range}
    lexicon_class = lexicon_module.ChooseModel()
    lexicon_part = await create_lexicon_part(lexicon_class, button_texts)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part=lexicon_part, lexicon_cache=False, dynamic_buttons=lexicon_class.dynamic_buttons)


    await callback.answer()
    await state.set_state(HybridChooseStates.select_complectation)

    '''Кэширование для кнопки НАЗАД'''
    # await backward_in_carpooling_controller(callback=callback, state=state)


async def choose_complectation_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    await cache_state(callback=callback, state=state)

    memory_storage = await state.get_data()
    if first_call:
        user_answer = int(callback.data.split('_')[-1])  # Второе слово - ключевое к значению бд
        await state.update_data(cars_model=user_answer)
        delete_mode = False
    else:
        delete_mode = True
        user_answer = memory_storage['cars_model']

    models_range = await AdvertRequester.get_advert_by(state_id=memory_storage['cars_state'],
                                                       brand_id=memory_storage['cars_brand'],
                                                       engine_type_id=memory_storage['cars_engine_type'],
                                                       model_id=user_answer)

    button_texts = {car.complectation for car in models_range}
    lexicon_class = lexicon_module.ChooseComplectation()
    lexicon_part = await create_lexicon_part(lexicon_class, button_texts)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part=lexicon_part, lexicon_cache=False, delete_mode=delete_mode, dynamic_buttons=lexicon_class.dynamic_buttons)

    await state.set_state(HybridChooseStates.select_color)

    await callback.answer()

async def choose_color_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


    await cache_state(callback=callback, state=state)

    memory_storage = await state.get_data()
    if first_call:
        user_answer = int(callback.data.split('_')[-1])  # Второе слово - ключевое к значению бд
        await state.update_data(cars_complectation=user_answer)
        delete_mode=True
    else:
        delete_mode=False
        user_answer = memory_storage['cars_complectation']

    models_range = await AdvertRequester.get_advert_by(state_id=memory_storage['cars_state'],
                                                       brand_id=memory_storage['cars_brand'],
                                                       engine_type_id=memory_storage['cars_engine_type'],
                                                       model_id=memory_storage['cars_model'],
                                                       complectation_id=user_answer)


    button_texts = {car.color for car in models_range}
    lexicon_class = lexicon_module.ChooseColor()
    lexicon_part = await create_lexicon_part(lexicon_class, button_texts)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part=lexicon_part, lexicon_cache=False, delete_mode=delete_mode,
                                                    dynamic_buttons=lexicon_class.dynamic_buttons)

    cars_type = int(memory_storage['cars_state'])
    if cars_type == 2:
        await state.set_state(SecondHandChooseStates.select_mileage)
    elif cars_type == 1:
        await state.set_state(HybridChooseStates.config_output)

    await callback.answer()

async def search_config_output_handler(callback: CallbackQuery, state: FSMContext):
    await cache_state(callback=callback, state=state)

    memory_storage = await state.get_data()
    user_answer = int(callback.data.split('_')[-1])  # Второе слово - ключевое к значению бд
    ic(memory_storage['cars_class'])
    if int(memory_storage['cars_class']) == 2:
        await state.update_data(cars_year_of_release=user_answer)


    elif int(memory_storage['cars_class']) == 1:
        ic()
        await state.update_data(cars_color=user_answer)

    formatted_config_output = await get_cars_data_pack(callback=callback, state=state)

    await state.update_data(buyer_id=str(callback.from_user.id))

    await callback.message.delete()

    pagination = BuyerCarsPagination(data=formatted_config_output, page_size=1, current_page=0)

    await pagination.send_page(request=callback, state=state)

    await callback.answer()




