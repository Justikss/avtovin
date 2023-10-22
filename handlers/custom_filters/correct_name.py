import importlib

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, chat

from handlers.state_handlers.buyer_registration_handlers import input_full_name


class CorrectName(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        memory_storage = await state.get_data()
        redis_storage = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        message_id = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':last_message')

        user_full_name = message.text
        formatted_full_name = user_full_name.split(' ')
        if 1 < len(formatted_full_name) < 4:
            for word in formatted_full_name:
                if not word.isalpha():
                    await chat.Chat.delete_message(self=message.chat, message_id=message_id)
                    return await input_full_name(request=message, state=state, incorrect=True)
            # await redis_storage.redis_data.delete_key(key=str(message.from_user.id) + ':last_user_message')
            return {'user_name': user_full_name}
        else:
            await chat.Chat.delete_message(self=message.chat, message_id=message_id)
            return await input_full_name(request=message, state=state, incorrect=True)
