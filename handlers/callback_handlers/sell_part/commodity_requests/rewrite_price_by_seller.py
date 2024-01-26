import importlib
from copy import copy
from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.input_rewrited_price_by_seller import RewritePriceBySellerStates


car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')
Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def rewrite_price_by_seller_handler(request: Union[CallbackQuery, Message], state: FSMContext, incorrect=False):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    #rewrite_price_by_seller
    request_data  = await message_editor.redis_data.get_data(
        key=f'{str(request.from_user.id)}:seller_request_data', use_json=True)
    car = await car_advert_requests_module\
        .AdvertRequester.get_where_id(request_data['car_id'])
    lexicon_part = copy(Lexicon_module\
                        .LexiconSellerRequests.input_new_price)
    if incorrect == '$':
      lexicon_part['message_text'] = f'''{lexicon_part['message_text']}\n{Lexicon_module.class_lexicon['incorrect_price_$']}'''
      delete_mode = True
      reply_message = request.message_id
    elif incorrect:
        lexicon_part['message_text'] += f'''\n{copy(Lexicon_module.LexiconSellerRequests.input_new_price_incorrect_message_text)}'''
        reply_message = request.message_id
        delete_mode = True
    else:
        reply_message = None
        delete_mode = True
    if not any((car.sum_price, car.dollar_price)):
        price = Lexicon_module.LEXICON['uzbekistan_valute'].replace('X', '0')
    else:
        price = Lexicon_module.LEXICON['uzbekistan_valute'].replace('X', str("{:,}".format(car.sum_price))) if car.sum_price else f'{str("{:,}".format(car.dollar_price))}$'

    lexicon_part['message_text'] = lexicon_part['message_text'].format(current_price=price)

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part, delete_mode=delete_mode, reply_message=reply_message)
    await state.set_state(RewritePriceBySellerStates.await_input)

async def get_input_to_rewrite_price_by_seller_handler(message: Message, state: FSMContext, price, head_valute):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    output_requests_module = importlib.import_module('handlers.callback_handlers.buy_part.backward_callback_handler')

    request_data  = await redis_module.redis_data.get_data(
        key=f'{str(message.from_user.id)}:seller_request_data', use_json=True)
    update_request = await car_advert_requests_module\
        .AdvertRequester.update_price(advert_id=request_data['car_id'], new_price=price, head_valute=head_valute)
    await state.clear()
    if update_request:
        await redis_module.redis_data.delete_key(key=str(message.from_user.id)+':seller_requests_pagination')
        await message_editor.travel_editor.edit_message(request=message, lexicon_key='',
                                                        lexicon_part=copy(Lexicon_module\
                                                                            .LexiconSellerRequests.succes_rewrite_price),
                                                        delete_mode=True)
    else:
        lexicon_part = copy(Lexicon_module\
                            .LexiconSellerRequests.input_new_price_car_dont_exists)
        await message_editor.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=lexicon_part, delete_mode=True)
