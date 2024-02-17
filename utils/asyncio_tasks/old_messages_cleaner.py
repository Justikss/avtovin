import asyncio
import importlib
import json
import logging

from aiogram import Bot

from database.data_requests.mailing_requests import collect_expired_viewed_mails

redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

class DeleteOldRedisKeys:
    def __init__(self):
        self.redis_base = redis_module.redis_data

    async def __call__(self, expired_mode=True):
        user_keys, user_id_to_message_id = await self.redis_base._find_users_with_expired_keys(expired_mode=expired_mode)
        ic(user_keys, user_id_to_message_id)
        data_to_chat_cleaning = await self.redis_base._delete_keys_for_users_without_active_keys(user_keys,
                                                                                                 user_id_to_message_id,
                                                                                                 expired_mode=expired_mode)
        return data_to_chat_cleaning




async def check_on_old_messages(bot: Bot):
    delete_old_redis_keys = DeleteOldRedisKeys()
    ic(delete_old_redis_keys)
    while True:
        deleted_data = await delete_old_redis_keys()
        expired_viewed_mailings = await collect_expired_viewed_mails()
        ic(expired_viewed_mailings)
        if expired_viewed_mailings:
            expired_mailings = {user_id: message_ids for user_id, message_ids in expired_viewed_mailings}
            ic(expired_mailings)
            if not deleted_data:
                deleted_data = {}
            deleted_data.update(expired_mailings)
        ic(deleted_data)
        if deleted_data:
            # logging.debug('Chat cleaner found: %s', json.dumps(deleted_data))
            for user_id, message_ids in deleted_data.items():
                try:
                    await bot.delete_messages(chat_id=user_id, message_ids=message_ids)
                except:
                    continue
                finally:
                    await asyncio.sleep(1)


        await asyncio.sleep(1740)
        # await asyncio.sleep(10)
