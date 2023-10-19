from typing import List, Tuple, Any

from aiogram.types import Message, CallbackQuery
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_chosen_search_config import redis_data
from database.data_requests.offers_requests import OffersRequester
from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import InlineCreator
from utils.Lexicon import LEXICON

async def pagination_state_data_unpack(callback: CallbackQuery, coding_in=False, vector: str = None) -> Tuple[int, Any]:
    redis_key = str(callback.from_user.id) + ':history_stack'
    if not coding_in:
        all_history = await redis_data.get_data(key=redis_key, use_json=True)
        history_stack = list(all_history.values())[0]
        stack_position = int(list(all_history.keys())[0])

        return stack_position, history_stack

    else:
        all_history = await redis_data.get_data(key=redis_key, use_json=True)
        history_stack = list(all_history.values())[0]
        stack_position = int(list(all_history.keys())[0])
        if vector == 'right':
            #current_page = (stack_position - 1) // 3 + 1
            #total_pages = (n - 1) // 3 + 1

            stack_position = stack_position+(len(history_stack) - int((stack_position % 3)))
            output_history_code = {stack_position: history_stack}

        elif vector == 'left':
            stack_position = stack_position-(len(history_stack) - int((stack_position % 3)))

            output_history_code = {stack_position: history_stack}


        await redis_data.set_data(key=redis_key, value=output_history_code)

async def history_view_system(callback, redis_key, edit_mode=False):
    pagination_redis_key = str(callback.from_user.id) + ':history_requests_pagination'
    # print('histor', type(all_history), all_history)
    stack_position, history_stack = await pagination_state_data_unpack(callback)
    history_part = history_stack[stack_position:]
    print('st', history_stack)
    print('part', history_part)
    for history_block in history_part:

        block_position = history_stack.index(history_block) + 1
        print(block_position != len(history_stack) - 1)
        print(block_position % 3, history_stack.index(history_block))
        if block_position != len(history_stack) and block_position % 3 != 0:
            print('yos:')

            if block_position == 1:
                pagination_redis_key += ':first'
            elif block_position == 2:
                pagination_redis_key += ':second'

            if not edit_mode:
                pre_message = await callback.message.answer(text=history_block)
                await redis_data.set_data(key=pagination_redis_key, value=pre_message.message_id)
            else:
                editable_message = await redis_data.get_data(key=pagination_redis_key)
                await callback.message.bot.edit_message_text(self=callback.message.bot,
                                                             chat_id=callback.message.chat.id,
                                                             message_id=int(editable_message),
                                                             text=history_block)

            print(await redis_data.get_data(key=pagination_redis_key))
        else:

            keyboard = await InlineCreator.create_markup(input_data=LEXICON['buttons_history_output'])
            pagination_redis_key += ':head'

            if not edit_mode:
                head_message = await callback.message.answer(text=history_block, reply_markup=keyboard)
                await redis_data.set_data(key=pagination_redis_key, value=head_message.message_id)
            else:
                editable_message = await redis_data.get_data(key=pagination_redis_key)
                await callback.message.bot.edit_message_text(self=callback.message.bot,
                                                             chat_id=callback.message.chat.id,
                                                             message_id=int(editable_message),
                                                             text=history_block,
                                                             reply_markup=keyboard)

            print(await redis_data.get_data(key=pagination_redis_key))
            # history_cache_value = {stack_position+len(history_part): history_stack}
            # await redis_data.set_data(key=redis_key, value=history_cache_value)
            return


async def format_history_data(offers_for_user: list) -> list:
    result_stack = list()

    for offer in offers_for_user:
        formatted_price = '{:,}'.format(offer.car.price).replace(',', '.')
        dealship_name = offer.seller.dealship_name
        if dealship_name:
            result_text = f'''
          🚘 Салон: {dealship_name}\n💰 Стоимость: {formatted_price}\nКонтакты салона:\n  - {offer.seller.phone_number}\n  - {offer.seller.dealship_address}
                        '''
        else:
            seller_full_name = offer.seller.surname + ' ' + offer.seller.name + ' ' + offer.seller.patronymic
            result_text = f'''
            👨🏻 Частное лицо: {seller_full_name}\n💰 Стоимость: {formatted_price}\nКонтакты:\n - {offer.seller.phone_number}
            '''
        result_stack.append(result_text)

    return result_stack

async def get_offers_history(callback: CallbackQuery):

    last_message = await redis_data.get_data(
        key=str(callback.from_user.id) + ':last_message')

    await callback.message.chat.delete_message(message_id=last_message) #Зарегать сюда собщение кнопочного оутпута

    offers = OffersRequester.get_for_buyer_id(buyer_id=callback.from_user.id)
    offers_stack = await format_history_data(offers_for_user=offers)
    redis_value = {0: offers_stack}
    redis_key = str(callback.from_user.id) + ':history_stack'

    await redis_data.set_data(key=redis_key, value=redis_value)

    test_res = await redis_data.get_data(key=redis_key, use_json=True)
    print(test_res)

    await history_view_system(callback=callback, redis_key=redis_key)

    await callback.answer(last_message)

'''Обработчики пагинации'''
async def history_pagination_right(callback: CallbackQuery):
    stack_position, history_stack = await pagination_state_data_unpack(callback)
    if stack_position == len(history_stack):
        await callback.answer('Больше сделок не планировалось.')
    else:
        await redis_data.set_data()


    await history_view_system