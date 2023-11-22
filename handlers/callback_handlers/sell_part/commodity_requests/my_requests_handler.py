import importlib
from aiogram.types import CallbackQuery

from database.data_requests.commodity_requests import CommodityRequester
from utils.Lexicon import LexiconSellerRequests as lexicon


async def get_lexicon_part(commodities) -> dict:
    '''Конструктор заготовки блока сообщений
    [Выбор марки автомобиля]'''
    car_brands = {car.brand for car in commodities}
    print('brands ', car_brands)
    lexicon_part = {'message_text': lexicon.select_brand_message_text,
                    'buttons': {lexicon.callback_prefix + brand: brand for brand in car_brands}}

    for callback_value, caption in lexicon.keyboard_end_part.items():
        lexicon_part['buttons'][callback_value] = caption
    print('lex_part ', lexicon_part)
    return lexicon_part

async def seller_requests_callback_handler(callback: CallbackQuery):
    '''Обработчик просмотра созданных продавцом заявок'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    media_group_delete_module = importlib.import_module('handlers.callback_handlers.sell_part.seller_main_menu')

    print('pre_deleter')
    await media_group_delete_module.delete_media_groups(request=callback)
    await message_editor.redis_data.delete_key(key=str(callback.from_user.id) + ':seller_requests_pagination')

    commodities = CommodityRequester.get_by_seller_id(seller_id=callback.from_user.id)

    if commodities:
        lexicon_part = await get_lexicon_part(commodities)
        await callback.answer()
        await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, dynamic_buttons=True)
    else:
        await callback.answer(lexicon.seller_does_have_active_requests_alert)
        return