from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.commodity_requests import CommodityRequester
from handlers.callback_handlers.search_auto_handler import travel_editor, redis_data
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_chosen_search_config import string_for_output
from states.new_car_choose_states import NewCarChooseStates
from states.hybrid_choose_states import HybridChooseStates
from states.second_hand_choose_states import SecondHandChooseStates


async def choose_brand_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(HybridChooseStates.select_brand)

    redis_key = str(callback.from_user.id) + ':cars_type'
    cars_type = await redis_data.get_data(redis_key)


    if cars_type == 'second_hand_cars':
        commodity_state = 'Б/У'
    elif cars_type == 'new_cars':
        commodity_state = 'Новая'

    models_range = CommodityRequester.get_for_request(state=commodity_state)
    await state.update_data(cars_state=commodity_state)

    await state.update_data(cars_class=commodity_state)

    button_texts = {car.brand for car in models_range}
    await travel_editor.edit_message(request=callback, lexicon_key='choose_brand',
                                     button_texts=button_texts, callback_sign='cars_brand:')

    await state.set_state(HybridChooseStates.select_model)


async def choose_model_handler(callback: CallbackQuery, state: FSMContext):
    memory_storage = await state.get_data()
    commodity_state = memory_storage['cars_state']

    user_answer = callback.data.split(':')[1] #Второе слово - ключевое к значению бд
    brand = user_answer
    await state.update_data(cars_brand=brand)

    models_range = CommodityRequester.get_for_request(state=commodity_state, brand=brand)

    button_texts = {car.model for car in models_range}
    await travel_editor.edit_message(request=callback, lexicon_key='choose_model', button_texts=button_texts,
                                     callback_sign='cars_model:')

    await state.set_state(HybridChooseStates.select_engine_type)


async def choose_engine_type_handler(callback: CallbackQuery, state: FSMContext):
    memory_storage = await state.get_data()
    user_answer = callback.data.split(':')[1]  # Второе слово - ключевое к значению бд
    await state.update_data(cars_model=user_answer)

    models_range = CommodityRequester.get_for_request(state=memory_storage['cars_state'],
                                                      brand=memory_storage['cars_brand'],
                                                      model=user_answer)

    button_texts = {car.engine_type for car in models_range}
    await travel_editor.edit_message(request=callback, lexicon_key='choose_engine_type', button_texts=button_texts,
                                     callback_sign='cars_engine_type:')

    if memory_storage['cars_class'] == 'Б/У':
        await state.set_state(SecondHandChooseStates.select_year)

    elif memory_storage['cars_class'] == 'Новая':
        await state.set_state(NewCarChooseStates.select_complectation)

async def search_config_output_handler(callback: CallbackQuery, state: FSMContext):
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

    elif memory_storage['cars_class'] == 'Новая':
        await state.update_data(cars_complectation=user_answer)

        result_model = CommodityRequester.get_for_request(state=memory_storage['cars_state'],
                                                          brand=memory_storage['cars_brand'],
                                                          model=memory_storage['cars_model'],
                                                          engine_type=memory_storage['cars_engine_type'],
                                                          complectation=user_answer)


    middle_cost = sum(car.price for car in result_model) // len(result_model)
    result_car = result_model[0]
    car_photo = result_car.photo_url
    print(car_photo)
    text_to_output = await string_for_output(callback=callback, car_photo=car_photo, middle_cost=middle_cost)

    await callback.message.answer(text=text_to_output)

    await callback.answer()




