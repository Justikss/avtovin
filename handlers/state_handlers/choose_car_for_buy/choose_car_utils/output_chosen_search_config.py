import importlib
from typing import Optional, List

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config_data.config import lifetime_of_redis_record_of_request_caching
from database.data_requests.car_advert_requests import AdvertRequester

from utils.Lexicon import LEXICON

async def get_seller_header(seller=None, car=None):
    message_text = LEXICON.get('chosen_configuration').get('message_text')
    if car:
        seller = car.seller

    if seller.dealship_name:
        seller_header = message_text.get('from_dealership').replace('X', seller.dealship_name).replace('Y', seller.dealship_address)
    else:
        seller_header = message_text.get('from_seller').replace('X', ' '.join([seller.name, seller.surname, seller.patronymic if seller.patronymic else '']))

    return seller_header

async def get_output_string(car, message_text, cars_state):
    seller_header = await get_seller_header(car=car)

    canon_string = f'''{message_text['your_configs']}\n{seller_header}\n\n{message_text['car_state']} {car.state.name}\n{message_text['engine_type']} {car.engine_type.name}\n{message_text['brand']} {car.complectation.model.brand.name}\n{message_text['model']} {car.complectation.model.name}\n{message_text['complectation']} {car.complectation.name}\n'''

    if int(cars_state) == 2:
        middle_string = f'''{message_text['color']} {car.color.name}\n{message_text['year']} {car.year.name}\n{message_text['mileage']} {car.mileage.name}\n'''

    elif int(cars_state) == 1:
        middle_string = ''

    cost_string = f'''{message_text['cost'].replace('X', car.price)}'''
    result_string = f'{canon_string}{middle_string}{cost_string}'
    return result_string


async def get_cars_data_pack(callback: CallbackQuery, state: FSMContext, car_models=None):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    cached_requests_module = importlib.import_module('database.data_requests.offers_requests')


    redis_key = str(callback.from_user.id) + ':cars_type'
    cars_state = await redis_module.redis_data.get_data(redis_key)

    lexicon_part = LEXICON.get('chosen_configuration')
    message_text = lexicon_part.get('message_text')

    data_stack = []
    ic()
    ic(car_models)
    if not car_models:
        first_view_mode = True
        memory_storage = await state.get_data()
        ic(memory_storage)

        car_state = memory_storage.get('cars_state')
        brand = memory_storage.get('cars_brand')
        model = memory_storage.get('cars_model')
        engine_type = memory_storage.get('cars_engine_type')
        year_of_release = memory_storage.get('cars_year_of_release')
        mileage = memory_storage.get('cars_mileage')
        color = memory_storage.get('cars_color')
        complectation = str(memory_storage.get('cars_complectation'))
        ic(car_state)


        car_models = await AdvertRequester.get_advert_by(state_id=car_state,
                                                         engine_type_id=engine_type,
                                                         brand_id=brand,
                                                         model_id=model,
                                                         complectation_id=complectation,
                                                         color_id=color,
                                                         mileage_id=mileage,
                                                         year_of_release_id=year_of_release
                                                         )
        ic(car_models)
    else:
        first_view_mode = False
    ic()
    ic(car_models)
    for car in car_models:
        result_string = await get_output_string(car, message_text, cars_state)

        photo_album = await AdvertRequester.get_photo_album_by_advert_id(car.id)

        result_part = {'car_id': car.id, 'message_text': result_string, 'album': photo_album}
        data_stack.append(result_part)

    if first_view_mode:
        await cached_requests_module.CachedOrderRequests.set_cache(buyer_id=callback.from_user.id, car_data=data_stack)


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


