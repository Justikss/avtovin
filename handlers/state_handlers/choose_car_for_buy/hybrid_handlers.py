import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.utils.set_color_1_in_last_position import set_other_color_on_last_position
from database.tables.car_configurations import CarEngine
from handlers.callback_handlers.hybrid_part import return_main_menu

# from database.data_requests.offers_requests import CachedOrderRequests
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_cars_pagination_system.pagination_system_for_buyer import \
    BuyerCarsPagination
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler import output_choose
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_chosen_search_config import get_cars_data_pack
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.states_cacher import cache_state
from handlers.utils.message_answer_without_callback import send_message_answer
from states.hybrid_choose_states import HybridChooseStates
from states.second_hand_choose_states import SecondHandChooseStates
from handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers import create_lexicon_part

config_module = importlib.import_module('config_data.config')
car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')

async def search_auto_callback_handler(callback: CallbackQuery, state: FSMContext):
    choose_car_states_module = importlib.import_module('states.hybrid_choose_states')
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await message_editor.travel_editor.edit_message(lexicon_key='search_car', request=callback)

    # redis_key = str(callback.from_user.id) + ':last_lexicon_code'
    # await message_editor.redis_data.set_data(redis_key, 'search_car')
    await state.set_state(choose_car_states_module.HybridChooseStates.select_engine_type)




async def choose_engine_type_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    ic()
    user_id = callback.from_user.id
    redis_key = str(user_id) + ':cars_type'

    if callback.data[-1].isdigit():
        commodity_state = callback.data.split('_')[-1]
        await message_editor.redis_data.set_data(redis_key, commodity_state)
        cars_type = commodity_state
    else:
        cars_type = await message_editor.redis_data.get_data(redis_key)

    await cache_state(callback=callback, state=state, first=True)

    # models_range = await car_advert_requests_module\
    # .AdvertRequester.get_advert_by(state_id=cars_type)
    models_range = await car_advert_requests_module\
        .AdvertRequester.get_advert_by(state_id=cars_type, buyer_search_mode=callback.from_user.id)
    ic(models_range)
    if not models_range:
        return await message_editor.travel_editor.edit_message(request=callback, lexicon_key='cars_not_found', lexicon_cache=False)


    await state.update_data(cars_state=cars_type)
    ic(cars_type)
    await state.update_data(cars_class=cars_type)

    lexicon_class = lexicon_module.ChooseEngineType
    lexicon_part = await create_lexicon_part(lexicon_class, models_range)
    lexicon_part['buttons']['width'] = lexicon_class.width
    ic(lexicon_part)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                     lexicon_part=lexicon_part, lexicon_cache=False, dynamic_buttons=lexicon_class.dynamic_buttons)

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
    else:
        user_answer = memory_storage['cars_engine_type']

    models_range = await car_advert_requests_module\
        .AdvertRequester.get_advert_by(state_id=memory_storage['cars_state'],
                                        engine_type_id=user_answer,
                                       buyer_search_mode=callback.from_user.id
                                                    )

    # button_texts = {car.complectation.model.brand for car in models_range}
    lexicon_class = lexicon_module.ChooseBrand
    await output_choose(callback, state, lexicon_class, models_range, config_module\
                        .car_configurations_in_keyboard_page)

    # await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
    #                                  lexicon_part=lexicon_part, lexicon_cache=False, dynamic_buttons=lexicon_class.dynamic_buttons)


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


    models_range = await car_advert_requests_module\
        .AdvertRequester.get_advert_by(state_id=commodity_state, brand_id=brand, engine_type_id=engine_type,
                                       buyer_search_mode=callback.from_user.id)

    # button_texts = {car.complectation.model for car in models_range}
    lexicon_class = lexicon_module.ChooseModel
    await output_choose(callback, state, lexicon_class, models_range, config_module\
                        .car_configurations_in_keyboard_page)

    # await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
    #                                                 lexicon_part=lexicon_part, lexicon_cache=False, dynamic_buttons=lexicon_class.dynamic_buttons)


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

    models_range = await car_advert_requests_module\
        .AdvertRequester.get_advert_by(state_id=memory_storage['cars_state'],
                                                       brand_id=memory_storage['cars_brand'],
                                                       engine_type_id=memory_storage['cars_engine_type'],
                                                       model_id=user_answer,
                                       buyer_search_mode=callback.from_user.id)

    # button_texts = {car.complectation for car in models_range}
    lexicon_class = lexicon_module.ChooseComplectation
    ic(lexicon_class.__dict__)
    await output_choose(callback, state, lexicon_class, models_range, config_module\
                        .car_configurations_in_keyboard_page)
    # await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
    #                                                 lexicon_part=lexicon_part, lexicon_cache=False, delete_mode=delete_mode, dynamic_buttons=lexicon_class.dynamic_buttons)

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
        delete_mode=False
    else:
        delete_mode=True
        user_answer = memory_storage.get('cars_complectation')

    models_range = await car_advert_requests_module\
        .AdvertRequester.get_advert_by(state_id=memory_storage['cars_state'],
                                                       brand_id=memory_storage['cars_brand'],
                                                       engine_type_id=memory_storage['cars_engine_type'],
                                                       model_id=memory_storage['cars_model'],
                                                       complectation_id=user_answer,
                                                       buyer_search_mode=callback.from_user.id)
    if models_range:
        models_range = await set_other_color_on_last_position(models_range)

    # button_texts = {car.color for car in models_range}
    lexicon_class = lexicon_module.ChooseColor
    await output_choose(callback, state, lexicon_class, models_range, config_module\
                        .car_configurations_in_keyboard_page, need_last_buttons=False)

    # lexicon_part = await create_lexicon_part(lexicon_class, models_range)
    # await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
    #                                                 lexicon_part=lexicon_part, lexicon_cache=False, delete_mode=delete_mode,
    #                                                 dynamic_buttons=lexicon_class.dynamic_buttons)

    cars_type = int(memory_storage['cars_state'])
    ic(cars_type)
    if int(cars_type) == 2:
        await state.set_state(SecondHandChooseStates.select_mileage)
    elif int(cars_type) == 1:
        await state.set_state(HybridChooseStates.config_output)

    await callback.answer()

async def search_config_output_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    await cache_state(callback=callback, state=state)

    if first_call:
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

    try:
        await callback.message.delete()
    except:
        pass
    ic(formatted_config_output)
    if not formatted_config_output:
        Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
        await send_message_answer(callback, Lexicon_module.LEXICON['non_actiallity'])
        await return_main_menu.return_main_menu_callback_handler(callback, state)
        return

    pagination = BuyerCarsPagination(data=formatted_config_output, page_size=1, current_page=0)

    await pagination.send_page(request=callback, state=state)

    await callback.answer()




