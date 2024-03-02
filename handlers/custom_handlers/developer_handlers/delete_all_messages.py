import asyncio

from aiogram.types import Message

from database.data_requests.mailing_requests import collect_expired_viewed_mails


async def delete_all_messages_developer_handler(message: Message):
    await message.answer('Started')

    from utils.asyncio_tasks.old_messages_cleaner import DeleteOldRedisKeys
    from handlers.utils.delete_message import delete_message
    await delete_message(message, message.message_id)

    bot = message.bot
    delete_old_redis_keys = DeleteOldRedisKeys()
    ic(delete_old_redis_keys)
    deleted_data = await delete_old_redis_keys(expired_mode=False)
    expired_viewed_mailings = await collect_expired_viewed_mails(expired_mode=False)
    ic(expired_viewed_mailings)
    if expired_viewed_mailings:
        expired_mailings = {user_id: message_ids for user_id, message_ids in expired_viewed_mailings}
        ic(expired_mailings)
        if not deleted_data:
            deleted_data = {}
        deleted_data.update(expired_mailings)

    ic(deleted_data)
    if deleted_data:
        for user_id, message_ids in deleted_data.items():
            await bot.delete_messages(chat_id=user_id, message_ids=message_ids)
            await asyncio.sleep(1)

    from utils.redis_for_language import redis_data
    await redis_data.set_data('develop_moment_flag', 't')
    await message.answer('Successfully!')

    # await delete_message(message, bot_message)
