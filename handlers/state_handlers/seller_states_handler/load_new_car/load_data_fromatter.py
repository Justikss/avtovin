from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from typing import Union
from aiogram.fsm.context import FSMContext

from utils.Lexicon import LexiconCommodityLoader


async def data_formatter(request: Union[Message, CallbackQuery], state: FSMContext):
    '''Собирает сырые объекты в стэк данных по загружаемому автомобилю'''
    memory_storage = await state.get_data()

    # media_group_data = memory_storage.get('load_photo')
    # if media_group_data:
    #     group_data_key = [key for key, value in media_group_data.items()]
    #     print('memashpema: ', memory_storage.get('load_photo'))
    #     photo_media_group = [InputMediaPhoto(media=file_id) for file_id in memory_storage.get('load_photo')[group_data_key[0]]]
        # new_album = [InputMediaPhoto(media=file_id) for file_id in mediagroups[album_id]]

    #     photo_media_group = [InputMediaPhoto(media=photo['file_id']) for photo in memory_storage.get('load_photo')]
    #     print('photo_media_group ', photo_media_group)
    # else:
    #     photo_media_group = None

    data = {'seller_id': request.from_user.id,
    'state': LexiconCommodityLoader.load_commodity_state['buttons'][memory_storage['state_for_load']], 
    'engine_type': LexiconCommodityLoader.load_engine_type['buttons'][memory_storage['engine_for_load']], 
    'brand': LexiconCommodityLoader.load_commodity_brand['buttons'][memory_storage['brand_for_load']], 
    'model': LexiconCommodityLoader.load_commodity_model['buttons'][memory_storage['model_for_load']], 
    'complectation': LexiconCommodityLoader.load_commodity_complectation['buttons'][memory_storage['complectation_for_load']], 
    'year_of_release': LexiconCommodityLoader.load_commodity_year_of_realise['buttons'].get(memory_storage.get('year_for_load')), 
    'mileage': LexiconCommodityLoader.load_commodity_mileage['buttons'].get(memory_storage.get('mileage_for_load')), 
    'color': LexiconCommodityLoader.load_commodity_color['buttons'].get(memory_storage.get('color_for_load')), 
    'price': memory_storage['load_price'], 
    'photos': memory_storage.get('load_photo')}

    print('load_photos??: ', memory_storage.get('load_photo'))


    return data
