import asyncio
import importlib

from aiogram.types import Message

from handlers.utils.delete_message import delete_message

redis_module = importlib.import_module('utils.redis_for_language')
redis_get = redis_module.redis_data.get_data
redis_set = redis_module.redis_data.set_data
async def close_develop_moment_handler(message: Message):
    await message.answer('Started')

    develop_moment_notification_keys = [key async for key in redis_module.redis_data._scan_keys('*:sended_develop_moment_info')]
    if develop_moment_notification_keys:
        for key in develop_moment_notification_keys:
            message_id = await redis_get(key)
            if message_id:
                chat_id = int(key.split(':')[0])
                await delete_message(request=message, message_id=message_id, chat_id=chat_id)
                await asyncio.sleep(1)

    develop_moment_notification_keys.append('develop_moment_flag')
    await redis_module.redis_data.redis_base.delete(*develop_moment_notification_keys)
    # await redis_module.redis_data.redis_base.delete()
    await redis_module.redis_data.flushdb_action()
    await message.answer('Success')