from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import importlib

from handlers.callback_handlers.sell_part.commodity_requests.rewrite_price_by_seller import \
    rewrite_price_by_seller_handler
from handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers import input_price_to_load


class PriceIsDigit(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        '''Фильтр контроллирует вход числа во время загрузки нового товара'''
        redis_module = importlib.import_module('utils.redis_for_language')
        redis_key_user_message = str(message.from_user.id) + ':last_seller_message'
        redis_key_bot_message = str(message.from_user.id) + ':last_message'


        if message.text.isdigit():
            car_price = message.text
            await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            last_seller_message = await redis_module.redis_data.get_data(key=redis_key_user_message)
            if last_seller_message:
                try:
                    await message.bot.delete_message(chat_id=message.chat.id, message_id=last_seller_message)
                    await redis_module.redis_data.delete_key(key=redis_key_user_message)
                except: pass
            return {'car_price': car_price}
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
                await input_price_to_load(request=message, state=state, incorrect=True)