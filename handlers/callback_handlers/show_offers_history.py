import importlib
import math
from typing import List, Tuple, Any

import aiogram.exceptions
from aiogram.types import Message, CallbackQuery
from database.data_requests.offers_requests import OffersRequester
from utils.Lexicon import LEXICON


async def history_view_system(callback, vector=None, start_flag=None):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    inline_creator = importlib.import_module('keyboards.inline.kb_creator')  # Ленивый импорт



    lexicon_part = LEXICON['show_offers_history']
    print(lexicon_part)
    redis_key = str(callback.from_user.id) + ':history_stack'
    redis_storage = await redis_module.redis_data.get_data(key=redis_key, use_json=True)
    current_page, resend_head_message, history_stack = redis_storage[0], redis_storage[1], redis_storage[2]
    items_per_page = 3  # Количество элементов на каждой странице

    total_pages = len(history_stack) // items_per_page
    if len(history_stack) % items_per_page != 0:
        total_pages += 1

    if vector == 'right':
        if current_page < total_pages:
            current_page += 1
        else:
            await callback.answer(lexicon_part['no_more_pages'])
            return

    elif vector == 'left':
        if current_page > 1:
            current_page -= 1
        else:
            await callback.answer(lexicon_part['no_less_pages'])
            return



    start_index = (current_page - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(history_stack))
    if start_index < end_index:
        for message_block_index in range(start_index, end_index):
            block_position_index = message_block_index - start_index
            if block_position_index == 0 and start_index + 1 != end_index:
                pagination_redis_key = str(callback.from_user.id) + ':history_requests_pagination' + ':first'
                flag_pre = True
                current_last_pre_message = await redis_module.redis_data.get_data(key=pagination_redis_key)
                current_last_pre_message = int(current_last_pre_message[0])


            elif block_position_index == 1 and start_index + 2 != end_index:
                pagination_redis_key = str(callback.from_user.id) + ':history_requests_pagination' + ':second'
                flag_pre = True
                current_last_pre_message = await redis_module.redis_data.get_data(key=pagination_redis_key)
                current_last_pre_message = int(current_last_pre_message[0])


            else:
                if block_position_index == 0 and not start_flag:
                    first_last_message_key = str(callback.from_user.id) + ':history_requests_pagination' + ':first'
                    second_last_message_key = str(callback.from_user.id) + ':history_requests_pagination' + ':second'

                    first_last_message_id = await redis_module.redis_data.get_data(key=first_last_message_key)
                    second_last_message_id = await redis_module.redis_data.get_data(key=second_last_message_key)

                    await redis_module.redis_data.set_data(key=first_last_message_key, value=0)
                    await redis_module.redis_data.set_data(key=second_last_message_key, value=0)

                    await callback.message.bot.delete_message(chat_id=callback.message.chat.id,
                                                              message_id=int(first_last_message_id))
                    await callback.message.bot.delete_message(chat_id=callback.message.chat.id,
                                                              message_id=int(second_last_message_id))



                elif block_position_index == 1 and not start_flag:
                    second_last_message_key = str(callback.from_user.id) + ':history_requests_pagination' + ':second'

                    second_last_message_id = await redis_module.redis_data.get_data(key=second_last_message_key)

                    await redis_module.redis_data.set_data(key=second_last_message_key, value=0)

                    await callback.message.bot.delete_message(chat_id=callback.message.chat.id,
                                                              message_id=int(second_last_message_id))


                pagination_redis_key = str(callback.from_user.id) + ':history_requests_pagination' + ':head'
                keyboard = await inline_creator.InlineCreator.create_markup(input_data=LEXICON['buttons_history_output'])

                if start_flag or resend_head_message:
                    if resend_head_message:
                        last_head_message_id = await redis_module.redis_data.get_data(key=pagination_redis_key)
                        last_head_message_id = int(last_head_message_id)
                        await callback.message.bot.delete_message(chat_id=callback.message.chat.id,
                                                              message_id=last_head_message_id)

                    head_message = await callback.message.answer(text=history_stack[message_block_index], reply_markup=keyboard)
                    await redis_module.redis_data.set_data(key=pagination_redis_key, value=head_message.message_id)
                else:
                    try:
                        editable_message = await redis_module.redis_data.get_data(key=pagination_redis_key)
                        await callback.message.bot.edit_message_text(
                            chat_id=callback.message.chat.id,
                            message_id=int(editable_message),
                            text=history_stack[message_block_index],
                            reply_markup=keyboard)
                    except aiogram.exceptions.TelegramBadRequest:
                        await callback.answer()

                if block_position_index in (0, 1):
                    resend_head_message = True
                else:
                    resend_head_message = False

                redis_value = (current_page, resend_head_message, history_stack)
                await redis_module.redis_data.set_data(key=redis_key, value=redis_value)
                return

            if flag_pre == True:
                if start_flag or current_last_pre_message == 0:
                    pre_message = await callback.message.answer(text=history_stack[message_block_index])
                    await redis_module.redis_data.set_data(key=pagination_redis_key, value=pre_message.message_id)
                    # editable_message = await redis_module.redis_data.get_data(key=pagination_redis_key)
                else:
                    editable_message = await redis_module.redis_data.get_data(key=pagination_redis_key)
                    await callback.message.bot.edit_message_text(
                        chat_id=callback.message.chat.id,
                        message_id=int(editable_message),
                        text=history_stack[message_block_index])


async def format_history_data(offers_for_user: list) -> list:
    result_stack = list()
    lexicon_part = LEXICON['offer_parts']
    for offer in offers_for_user:
        offer_wire = await OffersRequester.get_wire_by_offer_id(offer.id)
        offer_cars = [offer.car_id for offer in offer_wire]
        car_price_sum = sum(car.price for car in offer_cars)
        average_price = car_price_sum // len(offer_cars)
        formatted_price = '{:,}'.format(average_price).replace(',', '.')
        dealship_name = offer.seller.dealship_name
        if dealship_name:
            result_text = f'''
          🚘 {lexicon_part['dealship_name']}: {dealship_name}\n💰 {lexicon_part['car_price']}: ~ {formatted_price}\n{lexicon_part['dealship_contacts']}:\n  - {offer.seller.phone_number}\n  - {offer.seller.dealship_address}
                        '''
        else:
            seller_full_name = offer.seller.surname + ' ' + offer.seller.name + ' ' + offer.seller.patronymic
            result_text = f'''
            👨🏻 {lexicon_part['individual']}: {seller_full_name}\n💰 {lexicon_part['car_price']}: {formatted_price}\n{lexicon_part['individual_contacts']}:\n - {offer.seller.phone_number}
            '''
        result_stack.append(result_text)

    return result_stack

async def get_offers_history(callback: CallbackQuery):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт


    lexicon_part = LEXICON['offer_parts']
    first_last_message_key = str(callback.from_user.id) + ':history_requests_pagination' + ':first'
    second_last_message_key = str(callback.from_user.id) + ':history_requests_pagination' + ':second'
    head_last_message_key = str(callback.from_user.id) + ':history_requests_pagination' + ':head'

    await redis_module.redis_data.set_data(key=first_last_message_key, value=0)
    await redis_module.redis_data.set_data(key=second_last_message_key, value=0)
    await redis_module.redis_data.set_data(key=head_last_message_key, value=0)

    last_message = await redis_module.redis_data.get_data(
        key=str(callback.from_user.id) + ':last_message')

    offers = await OffersRequester.get_for_buyer_id(buyer_id=callback.from_user.id)
    if not offers:
        await callback.answer(LEXICON["buyer_haven't_confirm_offers"])
    else:
        offers_stack = await format_history_data(offers_for_user=offers)
        redis_value = (0, False, offers_stack)
        redis_key = str(callback.from_user.id) + ':history_stack'
        print('last', last_message)
        if offers:
            await callback.message.chat.delete_message(message_id=last_message)  # Зарегать сюда собщение кнопочного оутпута

            await redis_module.redis_data.set_data(key=redis_key, value=redis_value)

            # test_res = await redis_module.redis_data.get_data(key=redis_key, use_json=True)
            # print(test_res)

            await history_view_system(callback=callback, vector='right', start_flag=True)

            await callback.answer(last_message)
        else:
            await callback.answer(lexicon_part['history_not_found'])


'''Обработчики пагинации'''
async def history_pagination_right(callback: CallbackQuery):
    await history_view_system(callback=callback, vector='right')

async def history_pagination_left(callback: CallbackQuery):
    await history_view_system(callback=callback, vector='left')


