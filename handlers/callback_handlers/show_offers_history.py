from aiogram.types import Message, CallbackQuery
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_chosen_search_config import redis_data
from database.data_requests.offers_requests import OffersRequester
from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import InlineCreator
from utils.Lexicon import LEXICON


async def history_view_system(callback, redis_key, edit_mode=False):
    all_history = await redis_data.get_data(key=redis_key, use_json=True)
    # print('histor', type(all_history), all_history)
    history_stack = list(all_history.values())[0]
    stack_position = int(list(all_history.keys())[0])
    history_part = history_stack[stack_position:]
    print('st', history_stack)
    print('part', history_part)
    for history_block in history_part:

        block_position = history_stack.index(history_block) + 1
        print(block_position != len(history_stack) - 1)
        print(block_position % 3, history_stack.index(history_block))
        if block_position != len(history_stack) and block_position % 3 != 0:
            print('yos:')
            if not edit_mode:
                pre_message = await callback.message.answer(text=history_block)
        else:
            print('last', history_block)
            keyboard = await InlineCreator.create_markup(input_data=LEXICON['buttons_history_output'])

            head_message = await callback.message.answer(text=history_block, reply_markup=keyboard)

            history_cache_value = {stack_position+len(history_part): history_stack}
            await redis_data.set_data(key=redis_key, value=history_cache_value)
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
