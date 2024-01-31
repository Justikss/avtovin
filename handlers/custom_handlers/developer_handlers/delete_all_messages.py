import asyncio

from aiogram.types import Message


async def delete_all_messages_developer_handler(message: Message):
    from utils.asyncio_tasks.old_messages_cleaner import DeleteOldRedisKeys
    from handlers.utils.delete_message import delete_message
    await delete_message(message, message.message_id)

    bot = message.bot
    delete_old_redis_keys = DeleteOldRedisKeys()
    ic(delete_old_redis_keys)
    deleted_data = await delete_old_redis_keys(expired_mode=False)
    ic(deleted_data)
    if deleted_data:
        for user_id, message_ids in deleted_data.items():
            await bot.delete_messages(chat_id=user_id, message_ids=message_ids)
            await asyncio.sleep(1)


    await message.answer('Successfully!')

    # await delete_message(message, bot_message)
