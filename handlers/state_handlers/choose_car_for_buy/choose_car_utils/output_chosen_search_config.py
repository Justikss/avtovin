import importlib
from typing import Optional, List

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config_data.config import lifetime_of_redis_record_of_request_caching
from database.data_requests.commodity_requests import CommodityRequester
from database.data_requests.offers_requests import CachedOrderRequests
from database.tables.commodity import Commodity
from utils.Lexicon import LEXICON

async def get_cars_data_pack(callback: CallbackQuery, state: FSMContext, car_models=None):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

    redis_key = str(callback.from_user.id) + ':cars_type'
    cars_state = await redis_module.redis_data.get_data(redis_key)

    lexicon_part = LEXICON.get('chosen_configuration')
    message_text = lexicon_part.get('message_text')

    data_stack = []
    if not car_models:
        first_view_mode = True
        memory_storage = await state.get_data()

        car_state = memory_storage.get('cars_state')
        brand = memory_storage.get('cars_brand')
        model = memory_storage.get('cars_model')
        engine_type = memory_storage.get('cars_engine_type')
        year_of_release = memory_storage.get('cars_year_of_release')
        mileage = memory_storage.get('cars_mileage')
        color = memory_storage.get('cars_color')
        complectation = str(memory_storage.get('cars_complectation'))
        ic(car_state)

        car_models = CommodityRequester.get_for_request(state=car_state,
                                                          brand=brand,
                                                          model=model,
                                                          engine_type=engine_type,
                                                          year_of_release=year_of_release,
                                                          mileage=mileage,
                                                          color=color,
                                                          complectation=complectation)

    else:
        first_view_mode = False
    car_ids = []

    for car in car_models:
        car_ids.append(car.car_id)
        if cars_state == 'second_hand_cars':
            result_string = f'''
                {message_text['your_configs']}\n{message_text['car_state']} {car.state}\n{message_text['engine_type']} {car.engine_type}\n{message_text['color']} {car.color}\n{message_text['model']} {car.model}\n{message_text['brand']} {car.brand}\n{message_text['complectation']} {car.complectation}\n{message_text['year']} {car.year_of_release}\n{message_text['mileage']} {car.mileage}\n{message_text['cost']} {car.price}'''

        elif cars_state == 'new_cars':
            result_string = f'''
                {message_text['your_configs']}\n{message_text['car_state']} {car.state}\n{message_text['engine_type']} {car.engine_type}\n{message_text['model']} {car.model}\n{message_text['brand']} {car.brand}\n{message_text['complectation']} {car.complectation}\n{message_text['cost']} {car.price}'''

        photo_album = CommodityRequester.get_photo_album_by_car_id(car_id=car.car_id)

        result_part = {'car_id': car.car_id, 'message_text': result_string, 'album': photo_album}
        data_stack.append(result_part)

    if first_view_mode:
        ic(data_stack)
        await CachedOrderRequests.set_cache(buyer_id=callback.from_user.id, car_data=data_stack)


    # await redis_module.redis_data.set_data(key=cache_non_confirm_cars_redis_key,
    #                                        value=data_stack, expire=lifetime_of_redis_record_of_request_caching)
    #
    # cache_redis_keys = await redis_module.redis_data.get_data(key=f'{str(callback.from_user.id)}:buyer_non_confirm_cars_redis_keys',
    #                                        use_json=True)
    # if not cache_redis_keys:
    #     cache_redis_keys = []
    # if cache_non_confirm_cars_redis_key in cache_redis_keys:
    #     pass
    # else:
    #     cache_redis_keys.append(cache_non_confirm_cars_redis_key)
    #
    # await redis_module.redis_data.set_data(key=f'{str(callback.from_user.id)}:buyer_non_confirm_cars_redis_keys',
    #                                        value=cache_redis_keys)

    return data_stack


