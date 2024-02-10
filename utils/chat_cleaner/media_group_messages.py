import importlib
from typing import Union

from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from handlers.utils.delete_message import delete_message


async def delete_media_groups(request: Union[CallbackQuery, Message]):
    redis_data_module = importlib.import_module('utils.redis_for_language')
    if isinstance(request, Message):
        message = request
    elif isinstance(request, CallbackQuery):
        message = request.message

    user_id = str(request.from_user.id)

    exist_media_group_message = await redis_data_module.redis_data.get_data(key=user_id + ':last_media_group', use_json=True)
    exist_check_seller_requests_pagination = await redis_data_module.redis_data.get_data(key=user_id + ':seller_media_group_messages', use_json=True)

    if exist_check_seller_requests_pagination:
        await redis_data_module.redis_data.delete_key(key=user_id + ':seller_media_group_messages')
        await delete_message(message, message_id=exist_check_seller_requests_pagination)

    if exist_media_group_message:

        await delete_message(message, message_id=exist_media_group_message)

        await redis_data_module.redis_data.delete_key(key=str(request.from_user.id) + ':last_media_group')
