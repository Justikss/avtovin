import asyncio
import importlib
from time import time

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.car_advert_requests import AdvertRequester
from handlers.utils.inline_buttons_pagination_heart import CachedRequestsView
from states.requests_by_seller import SellerRequestsState
from utils.Lexicon import LexiconSellerRequests as lexicon


async def get_car_brands(commodities) -> dict:
    '''Конструктор заготовки блока сообщений
    [Выбор марки автомобиля]'''
    car_brands = [car.complectation.model.brand for car in commodities]

    return {lexicon.callback_prefix + str(brand.id): brand.name for brand in car_brands}

async def seller_requests_callback_handler(callback: CallbackQuery, state: FSMContext, delete_mode=False):
    '''Обработчик просмотра созданных продавцом заявок'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    media_group_delete_module = importlib.import_module('handlers.callback_handlers.sell_part.seller_main_menu')

    print('pre_deleter')
    await media_group_delete_module.delete_media_groups(request=callback)
    await message_editor.redis_data.delete_key(key=str(callback.from_user.id) + ':seller_requests_pagination')
    ic()
    commodities = await AdvertRequester.get_advert_by_seller(seller_id=callback.from_user.id)
    ic(commodities)
    ic()
    if commodities:
        car_brands_keyboard_part = await get_car_brands(commodities)
        await callback.answer()
        await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon.select_brand_message_text, delete_mode=delete_mode)
        ic()
        await CachedRequestsView.choose_brand_for_output(callback, car_brands=car_brands_keyboard_part)
        await state.set_state(SellerRequestsState.await_input_brand)
        return True
    else:
        await callback.answer(lexicon.seller_does_have_active_requests_alert)
        return False