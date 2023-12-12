from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import importlib

from handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers import input_photo_to_load


class MessageIsPhoto(BaseFilter):
    '''Этот фильтр контролирует вхождение фотографии в конечное состояние загрузки товара'''
    async def chat_cleaner(self, trash_redis_keys, message):
        redis_module = importlib.import_module('utils.redis_for_language')
        user_id = str(message.from_user.id)
        for redis_key in trash_redis_keys:
            redis_key = user_id + redis_key
            last_message_id = await redis_module.redis_data.get_data(key=redis_key)
            if last_message_id:
                try:
                    await message.bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)
                    await redis_module.redis_data.delete_key(key=redis_key)
                except:
                    pass


    async def __call__(self, message: Message, state: FSMContext):
        '''Сама вызывающаяся функция фильтра. Контролирует вхождение фотографии'''
        redis_module = importlib.import_module('utils.redis_for_language')
        redis_key_seller = str(message.from_user.id) + ':last_seller_message'

        input_photo = message.photo
        ic(input_photo)
        reply_mode = False
        if not input_photo:
            reply_mode = True

        await self.chat_cleaner(trash_redis_keys=(':last_message', ':last_seller_message'),
                                 message=message)

        await redis_module.redis_data.set_data(key=redis_key_seller,
                                                value=message.message_id)
        ic()
        print('input_photo_to_load')#
        await input_photo_to_load(request=message, state=state, incorrect=True)#
