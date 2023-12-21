import asyncio
import importlib
from time import time

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.car_advert_requests import AdvertRequester
from states.requests_by_seller import SellerRequestsState


async def get_car_brands(car_brands) -> dict:
    '''Конструктор заготовки блока сообщений
    [Выбор марки автомобиля]'''
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    return {lexicon_module.LexiconSellerRequests.callback_prefix + str(brand.id): brand.name for brand in car_brands}

async def seller_requests_callback_handler(callback: CallbackQuery, state: FSMContext, delete_mode=False):
    '''Обработчик просмотра созданных продавцом заявок'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    media_group_delete_module = importlib.import_module('handlers.callback_handlers.sell_part.seller_main_menu')
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    cached_requests_view_module = importlib.import_module('handlers.utils.inline_buttons_pagination_heart')


    await media_group_delete_module.delete_media_groups(request=callback)
    await message_editor.redis_data.delete_key(key=str(callback.from_user.id) + ':seller_requests_pagination')
    ic()
    car_brands = await AdvertRequester.get_advert_brands_by_seller_id(seller_id=callback.from_user.id)
    ic(car_brands)
    ic()
    if car_brands:
        car_brands_keyboard_part = await get_car_brands(car_brands)
        await callback.answer()
        await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_module.LexiconSellerRequests.select_brand_message_text, delete_mode=delete_mode)
        ic()
        await cached_requests_view_module.CachedRequestsView.output_message_with_inline_pagination(callback, buttons_data=car_brands_keyboard_part, pagesize=8)
        await state.set_state(SellerRequestsState.await_input_brand)
        return True
    else:
        await callback.answer(lexicon_module.LexiconSellerRequests.seller_does_have_active_requests_alert)
        return False