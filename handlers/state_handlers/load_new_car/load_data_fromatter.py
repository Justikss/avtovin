from aiogram.types import CallbackQuery, Message
from typing import Union
from aiogram.fsm.context import FSMContext

from utils.Lexicon import LexiconCommodityLoader


async def data_formatter(request: Union[Message, CallbackQuery], state: FSMContext):
    '''Собирает сырые объекты в стэк данных по загружаемому автомобилю'''
    memory_storage = await state.get_data()

    data = {'seller_id': request.from_user.id, 
    'brand': LexiconCommodityLoader.load_commodity_brand['buttons'][memory_storage['brand_for_load']], 
    'model': LexiconCommodityLoader.load_commodity_model['buttons'][memory_storage['model_for_load']], 
    'engine_type': LexiconCommodityLoader.load_engine_type['buttons'][memory_storage['engine_for_load']], 
    'year_of_release': LexiconCommodityLoader.load_commodity_year_of_realise.get(memory_storage.get('load_year')), 
    'complectation': LexiconCommodityLoader.load_commodity_complectation['buttons'][memory_storage['complectation_for_load']], 
    'mileage': LexiconCommodityLoader.load_commodity_mileage.get(memory_storage.get('load_mileage')), 
    'state': LexiconCommodityLoader.load_commodity_state['buttons'][memory_storage['state_for_load']], 
    'color': LexiconCommodityLoader.load_commodity_color.get(memory_storage.get('load_color')), 
    'price': memory_storage['load_price'], 
    'photo_url': memory_storage.get('load_photo')}

    return data