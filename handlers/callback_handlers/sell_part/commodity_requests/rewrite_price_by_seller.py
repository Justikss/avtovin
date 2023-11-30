import importlib
from copy import copy
from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.data_requests.car_advert_requests import AdvertRequester
from states.input_rewrited_price_by_seller import RewritePriceBySellerStates
from utils.Lexicon import LexiconSellerRequests



async def rewrite_price_by_seller_handler(request: Union[CallbackQuery, Message], state: FSMContext, incorrect=False):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    #rewrite_price_by_seller
    request_data  = await redis_module.redis_data.get_data(
        key=f'{str(request.from_user.id)}:seller_request_data', use_json=True)
    car = await AdvertRequester.get_where_id(request_data['car_id'])
    lexicon_part = copy(LexiconSellerRequests.input_new_price)
    if incorrect:
        lexicon_part['message_text'] = copy(LexiconSellerRequests.input_new_price_incorrect_message_text)
        reply_message = request.message_id
        delete_mode = False
    else:
        reply_message = None
        delete_mode = True
    lexicon_part['message_text'] = lexicon_part['message_text'].replace('X', str(car.price))

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part, delete_mode=delete_mode, reply_message=reply_message)
    await state.set_state(RewritePriceBySellerStates.await_input)

async def get_input_to_rewrite_price_by_seller_handler(message: Message, state: FSMContext, car_price):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    output_requests_module = importlib.import_module('handlers.callback_handlers.buy_part.backward_callback_handler')

    request_data  = await redis_module.redis_data.get_data(
        key=f'{str(message.from_user.id)}:seller_request_data', use_json=True)
    update_request = await AdvertRequester.update_price(advert_id=request_data['car_id'], new_price=car_price)
    await state.clear()
    if update_request:
        # return await output_sellers_commodity_page(request=message, state=state)
        # car_brand = await redis_module.redis_data.get_data(
        #     key=str(message.from_user.id) + ':sellers_requests_car_brand_cache')
        # pagination_data = await redis_module.redis_data.get_data(key=str(message.from_user.id)+':seller_requests_pagination', use_json=True)
        await redis_module.redis_data.delete_key(key=str(message.from_user.id)+':seller_requests_pagination')
        await message_editor.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=copy(LexiconSellerRequests.succes_rewrite_price), delete_mode=True)
        # await output_requests_module.output_sellers_requests_by_car_brand_handler(message, state, chosen_brand=car_brand)
    else:
        lexicon_part = copy(LexiconSellerRequests.input_new_price_car_dont_exists)
        await message_editor.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=lexicon_part, delete_mode=True)
