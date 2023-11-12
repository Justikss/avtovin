import importlib
from typing import Union

from aiogram.types import Message, CallbackQuery


async def delete_media_groups(request: Union[CallbackQuery, Message]):
    redis_data_module = importlib.import_module('utils.redis_for_language')

    if isinstance(request, Message):
        message = request
    elif isinstance(request, CallbackQuery):
        message = request.message

    exist_media_group_message = await redis_data_module.redis_data.get_data(key=str(request.from_user.id) + ':last_media_group', use_json=True)
    if exist_media_group_message:
        try:
            print('tryrtyrty ', exist_media_group_message)
            [await request.bot.delete_message(chat_id=message.chat.id,
                                               message_id=message_id) for message_id in exist_media_group_message]
            await redis_data_module.redis_data.delete_key(key=str(request.from_user.id) + ':last_media_group')
        except Exception as ex:
            print(ex)
            pass
