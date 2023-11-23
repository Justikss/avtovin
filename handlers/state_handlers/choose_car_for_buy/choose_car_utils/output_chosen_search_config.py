import importlib
from typing import Optional, List

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.commodity_requests import CommodityRequester
from database.tables.commodity import Commodity
from utils.Lexicon import LEXICON

async def get_cars_data_pack(callback: CallbackQuery, state: FSMContext):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

    redis_key = str(callback.from_user.id) + ':cars_type'
    cars_state = await redis_module.redis_data.get_data(redis_key)

    lexicon_part = LEXICON.get('chosen_configuration')
    message_text = lexicon_part.get('message_text')

    data_stack = []

    memory_storage = await state.get_data()


    car_models = CommodityRequester.get_for_request(state=memory_storage.get('cars_state'),
                                                      brand=memory_storage.get('cars_brand'),
                                                      model=memory_storage.get('cars_model'),
                                                      engine_type=memory_storage.get('cars_engine_type'),
                                                      year_of_release=memory_storage.get('cars_year_of_release'),
                                                      mileage=memory_storage.get('cars_mileage'),
                                                      color=memory_storage.get('cars_color'),
                                                      complectation=str(memory_storage.get('cars_complectation')))

    for car in car_models:

        if cars_state == 'second_hand_cars':
            result_string = f'''
                {message_text['your_configs']}\n{message_text['engine_type']} {car.engine_type}\n{message_text['color']} {car.color}\n{message_text['model']} {car.model}\n{message_text['brand']} {car.brand}\n{message_text['complectation']} {car.complectation}\n{message_text['year']} {car.year_of_release}\n{message_text['mileage']} {car.mileage}\n{message_text['cost']} {car.price}'''

        elif cars_state == 'new_cars':
            result_string = f'''
                {message_text['your_configs']}\n{message_text['engine_type']} {car.engine_type}\n{message_text['model']} {car.model}\n{message_text['brand']} {car.brand}\n{message_text['complectation']} {car.complectation}\n{message_text['cost']} {car.price}'''

        photo_album = CommodityRequester.get_photo_album_by_car_id(car_id=car.car_id)

        result_part = {'car_id': car.car_id, 'message_text': result_string, 'album': photo_album}
        data_stack.append(result_part)

    return data_stack


redis_key = str() + ':selected_search_buy_config'
#
# brand = str(memory_storage['cars_brand'])
# model = str(memory_storage['cars_model'])
# engine = str(memory_storage['cars_engine_type'])
# year = str(user_answer)
# mileage = str(memory_storage['cars_mileage'])
# color = str(memory_storage['cars_color'])
# complectation = str(memory_storage['cars_complectation'])
#
# redis_value = {'cars_year_of_release': year, 'cars_brand': brand, 'cars_model': model, 'cars_engine_type': engine,
#                'cars_mileage': mileage, 'cars_color': color, 'cars_complectation': complectation}
#
# brand = str(memory_storage['cars_brand'])
# model = str(memory_storage['cars_model'])
# engine = str(memory_storage['cars_engine_type'])
# complectation = str(user_answer)
# year = None
# mileage = None
# color = None
#
# redis_value = {'cars_year_of_release': None, 'cars_brand': brand, 'cars_model': model, 'cars_engine_type': engine,
#                'cars_mileage': None, 'cars_color': None, 'cars_complectation': complectation}
#
# redis_value['average_cost'] = average_cost
# await redis_module.redis_data.set_data(key=redis_key, value=redis_value)