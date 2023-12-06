import asyncio
import importlib

from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from typing import Union
from aiogram.fsm.context import FSMContext

from database.data_requests.car_configurations_requests import CarConfigs
from utils.Lexicon import LexiconCommodityLoader


async def data_formatter(request: Union[Message, CallbackQuery], state: FSMContext, id_values=False):
    '''Собирает сырые объекты в стэк данных по загружаемому автомобилю'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    memory_storage = await state.get_data()

    sub_data = {'seller_id': request.from_user.id,
    'state': memory_storage['state_for_load'],
    'engine_type': memory_storage['engine_for_load'],
    'brand': memory_storage['brand_for_load'],
    'model': memory_storage['model_for_load'],
    'complectation': memory_storage['complectation_for_load'],
    'year_of_release': memory_storage.get('year_for_load'),
    'mileage': memory_storage.get('mileage_for_load'),
    'color': memory_storage.get('color_for_load'),
    'price': memory_storage['load_price'], 
    'photos': memory_storage.get('load_photo')}
    ic(sub_data)
    await message_editor.redis_data.set_data(key=f'{str(request.from_user.id)}:boot_advert_ids_kwargs', value=sub_data)
    
    result_data = dict()
    ic(sub_data)
    if not id_values:
        for key, value in sub_data.items():
            if key not in ('seller_id', 'price', 'photos') and value != None:
                ic(key, value)
                if str(value).isdigit():
                    value = await CarConfigs.get_by_id(key, value)
                    value = value.name


                ic(key, value)

                ic(key, value)
                ic()
            result_data[key] = value
    else:
        result_data = sub_data

    print('load_photos??: ', memory_storage.get('load_photo'))
    ic(sub_data)
    ic(result_data)
    return result_data
