import importlib
from typing import Union

from aiogram.types import Message, CallbackQuery


async def delete_media_groups(request: Union[CallbackQuery, Message]):
    redis_data_module = importlib.import_module('utils.redis_for_language')
    print('in delete_media_groups')
    if isinstance(request, Message):
        message = request
    elif isinstance(request, CallbackQuery):
        message = request.message

    user_id = str(request.from_user.id)

    exist_media_group_message = await redis_data_module.redis_data.get_data(key=user_id + ':last_media_group', use_json=True)
    exist_check_seller_requests_pagination = await redis_data_module.redis_data.get_data(key=user_id + ':seller_media_group_messages', use_json=True)
    # await redis_data_module.redis_data.delete_key(key=user_id + ':seller_requests_pagination')

    if exist_check_seller_requests_pagination:
        await redis_data_module.redis_data.delete_key(key=user_id + ':seller_media_group_messages')
        print('exist_check_seller_requests_pagination ', exist_check_seller_requests_pagination)
        for message_id in exist_check_seller_requests_pagination:
            try:
                await request.bot.delete_message(chat_id=message.chat.id,
                                                  message_id=message_id)
            except Exception as ex:
                print(ex)
                pass




    if exist_media_group_message:
        if isinstance(exist_media_group_message, int):
            message_id = exist_media_group_message
            try:
                await request.bot.delete_message(chat_id=message.chat.id,
                                                 message_id=message_id)
                await redis_data_module.redis_data.delete_key(key=str(request.from_user.id) + ':last_media_group')
            except Exception as ex:
                print(ex)
                pass

        else:

            for message_id in exist_media_group_message:
                try:
                    await request.bot.delete_message(chat_id=message.chat.id,
                                                       message_id=message_id)
                    await redis_data_module.redis_data.delete_key(key=str(request.from_user.id) + ':last_media_group')
                except Exception as ex:
                    print(ex)
                    pass
