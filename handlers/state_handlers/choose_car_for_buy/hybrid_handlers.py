import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.commodity_requests import CommodityRequester
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_chosen_search_config import string_for_output
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.states_cacher import cache_state
from states.new_car_choose_states import NewCarChooseStates
from states.hybrid_choose_states import HybridChooseStates
from states.second_hand_choose_states import SecondHandChooseStates

from utils.Lexicon import LEXICON



async def choose_brand_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await cache_state(callback=callback, state=state, first=True)

    redis_key = str(callback.from_user.id) + ':cars_type'
    cars_type = await message_editor.redis_data.get_data(redis_key)


    if cars_type == 'second_hand_cars':
        commodity_state = 'Б/У'
    elif cars_type == 'new_cars':
        commodity_state = 'Новая'

    models_range = CommodityRequester.get_for_request(state=commodity_state)
    if not models_range:
        return await message_editor.travel_editor.edit_message(request=callback, lexicon_key='cars_not_found', lexicon_cache=False)


    await state.update_data(cars_state=commodity_state)

    await state.update_data(cars_class=commodity_state)

    button_texts = {car.brand for car in models_range}
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='choose_brand',
                                     button_texts=button_texts, callback_sign='cars_brand:', lexicon_cache=False)

    '''Кэширование для кнопки НАЗАД'''
    # await backward_in_carpooling_controller(callback=callback, state=state)

    await state.set_state(HybridChooseStates.select_model)


async def choose_model_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await cache_state(callback=callback, state=state)

    memory_storage = await state.get_data()
    commodity_state = memory_storage['cars_state']

    if first_call:
        user_answer = callback.data.split(':')[1] #Второе слово - ключевое к значению бд
        brand = user_answer
        await state.update_data(cars_brand=brand)
    else:
        brand = memory_storage['cars_brand']


    models_range = CommodityRequester.get_for_request(state=commodity_state, brand=brand)

    button_texts = {car.model for car in models_range}
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='choose_model', button_texts=button_texts,
                                     callback_sign='cars_model:', lexicon_cache=False)

    '''Кэширование для кнопки НАЗАД'''
    # await backward_in_carpooling_controller(callback=callback, state=state)
    await state.set_state(HybridChooseStates.select_engine_type)

async def choose_engine_type_handler(callback: CallbackQuery, state: FSMContext, first_call=True):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await cache_state(callback=callback, state=state)

    memory_storage = await state.get_data()
    if first_call:
        user_answer = callback.data.split(':')[1]  # Второе слово - ключевое к значению бд
        await state.update_data(cars_model=user_answer)
        print(user_answer)
    else:
        user_answer = memory_storage['cars_model']

    models_range = CommodityRequester.get_for_request(state=memory_storage['cars_state'],
                                                      brand=memory_storage['cars_brand'],
                                                      model=user_answer)

    button_texts = {car.engine_type for car in models_range}
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='choose_engine_type', button_texts=button_texts,
                                     callback_sign='cars_engine_type:', lexicon_cache=False)

    '''Кэширование для кнопки НАЗАД'''
    #await backward_in_carpooling_controller(callback=callback, state=state)

    if memory_storage['cars_class'] == 'Б/У':
        await state.set_state(SecondHandChooseStates.select_year)

    elif memory_storage['cars_class'] == 'Новая':
        await state.set_state(NewCarChooseStates.select_complectation)

async def search_config_output_handler(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await cache_state(callback=callback, state=state)

    memory_storage = await state.get_data()
    user_answer = callback.data.split(':')[1]  # Второе слово - ключевое к значению бд
    if memory_storage['cars_class'] == 'Б/У':
        await state.update_data(cars_color=user_answer)

        result_model = CommodityRequester.get_for_request(state=memory_storage['cars_state'],
                                                          brand=memory_storage['cars_brand'],
                                                          model=memory_storage['cars_model'],
                                                          engine_type=memory_storage['cars_engine_type'],
                                                          year_of_release=memory_storage['cars_year_of_release'],
                                                          mileage=memory_storage['cars_mileage'],
                                                          color=user_answer)

        brand = str(memory_storage['cars_brand'])
        model = str(memory_storage['cars_model'])
        engine = str(memory_storage['cars_engine_type'])
        year = str(memory_storage['cars_year_of_release'])
        mileage = str(memory_storage['cars_mileage'])
        color = str(user_answer)
        complectation = None

    elif memory_storage['cars_class'] == 'Новая':
        await state.update_data(cars_complectation=user_answer)

        result_model = CommodityRequester.get_for_request(state=memory_storage['cars_state'],
                                                          brand=memory_storage['cars_brand'],
                                                          model=memory_storage['cars_model'],
                                                          engine_type=memory_storage['cars_engine_type'],
                                                          complectation=user_answer)

        brand = str(memory_storage['cars_brand'])
        model = str(memory_storage['cars_model'])
        engine = str(memory_storage['cars_engine_type'])
        complectation = str(user_answer)
        year = None
        mileage = None
        color = None

    average_cost = sum(car.price for car in result_model) // len(result_model)
    print(model)
    formatted_config_output = await string_for_output(callback=callback,
                                                      average_cost=average_cost,
                                                      year=year, mileage=mileage,
                                                      color=color, brand=brand,
                                                      model=model, engine=engine,
                                                      complectation=complectation)

    range_car_id = [str(car.car_id) for car in result_model]
    await state.update_data(offer_cars_range=range_car_id)
    await state.update_data(buyer_id=str(callback.from_user.id))

    result_car = result_model[0]
    car_photo = result_car.photo_url

    await callback.message.delete()

    photo = car_photo
    keyboard = await message_editor.InlineCreator.create_markup(input_data=LEXICON.get('chosen_configuration'))
    message_object = await callback.message.answer_photo(photo=photo, caption=formatted_config_output, reply_markup=keyboard)
    await message_editor.redis_data.set_data(str(callback.from_user.id) + ':last_message', message_object.message_id)

    '''Кэширование для кнопки НАЗАД'''
    #await backward_in_carpooling_controller(callback=callback, state=state)

    await callback.answer()




