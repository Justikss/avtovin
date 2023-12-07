from copy import copy

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import importlib

from handlers.callback_handlers.sell_part.commodity_requests.rewrite_price_by_seller import \
    rewrite_price_by_seller_handler
from handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers import input_price_to_load
from utils.get_currency_sum_usd import convertator


class PriceIsDigit(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        '''Фильтр контроллирует вход числа во время загрузки нового товара'''
        redis_module = importlib.import_module('utils.redis_for_language')
        redis_key_user_message = str(message.from_user.id) + ':last_seller_message'
        redis_key_bot_message = str(message.from_user.id) + ':last_message'
        message_text = copy(message.text)

        if '$' in message_text:
            ic()
            message_text = message_text.replace('$', ' ').strip()
            dollar_cost = True
            ic(message_text)
        else:
            dollar_cost = False
        if message_text.isdigit():
            ic(message.text.isdigit())
            car_price = int(message_text)
            await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            last_seller_message = await redis_module.redis_data.get_data(key=redis_key_user_message)
            if last_seller_message:
                try:
                    await message.bot.delete_message(chat_id=message.chat.id, message_id=last_seller_message)
                    await redis_module.redis_data.delete_key(key=redis_key_user_message)
                except: pass
            ic()
            head_valute = 'sum' if not dollar_cost else 'usd'
            ic(head_valute)
            await state.update_data(head_valute=head_valute)
            return {'price': car_price, 'head_valute': head_valute}
        else:
            last_seller_message = await redis_module.redis_data.get_data(key=redis_key_user_message)
            last_bot_message = await redis_module.redis_data.get_data(key=redis_key_bot_message)

            if last_seller_message:
                try:
                    await message.bot.delete_message(chat_id=message.chat.id, message_id=last_seller_message)
                    await redis_module.redis_data.delete_key(key=redis_key_user_message)
                    
                except:
                    pass
            if last_bot_message:
                try:
                    await message.bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message)
                    await redis_module.redis_data.delete_key(key=redis_key_bot_message)
                    
                except:
                    pass

            await redis_module.redis_data.set_data(key=redis_key_user_message, 
                                                    value=message.message_id)
            current_state = await state.get_state()
            if str(current_state) == 'RewritePriceBySellerStates:await_input':
                await rewrite_price_by_seller_handler(message, state, incorrect=True)
            else:
                print('go_to_price')
                ic()
                await input_price_to_load(request=message, state=state, incorrect=True)