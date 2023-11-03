from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Union
import importlib

from handlers.state_handlers.load_new_car.hybrid_handlers import input_photo_to_load


class MessageIsPhoto(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        redis_module = importlib.import_module('utils.redis_for_language')
        redis_key = str(message.from_user.id) + ':last_seller_message'

        input_data = message.text
        print('indat: ', input_data)
        if message:
            return {'photo_url': message.text}
        else:
            last_seller_message = await redis_module.redis_data.get_data(key=redis_key)
            if last_seller_message:
                try:
                    await message.bot.delete_message(chat_id=message.chat.id, message_id=last_seller_message)
                    await redis_module.redis_data.delete_key(key=redis_key)
                except:
                    pass

            await redis_module.redis_data.set_data(key=redis_key, 
                                                    value=message.message_id)

            await input_photo_to_load(message=message, state=state, incorrect=True)


