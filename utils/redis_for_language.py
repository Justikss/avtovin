import asyncio
import json
import traceback
from typing import Union
from redis import asyncio as aioredis


class RedisRequester:
    def __init__(self):
        self.pool = aioredis.ConnectionPool(
            host='localhost',
            decode_responses=True
        )
        self.redis_base = aioredis.StrictRedis(
            connection_pool=self.pool
        )
        self.scan_count = 300
        self.keys_storage = {
    'messages': (':last_user_message', ':last_message', ':last_seller_message',
                 '_notification', ':bot_header_message',
                 ':seller_media_group_messages', ':last_media_group'
    )#,
    # 'dependencies': (':inline_buttons_pagination_data', ':buyer_cars_pagination', ':language',
    #                  ':can_edit_seller_boot_commodity', ':boot_advert_ids_kwargs', ':state_history_stack',
    #                  ':structured_boot_data', ':seller_registration_mode', ':user_state',
    #                  ':sellers_requests_car_brand_cache', ':return_path_after_delete_car',
    #                  ':chat_id'
    #
    # )
}

    #
    # async def check_ttls(self, key: str):
    #
    #     ttl = await self.redis_base.ttl(key)
    #
    #     return ttl



    async def _find_users_with_expired_keys(self):
        user_keys = {}
        user_id_to_message_id = {}
        for key_pattern in self.keys_storage['messages']:
            async for key in self._scan_keys(f'*{key_pattern}'):

                user_id = key.split(':')[0]
                ttl = await self.redis_base.ttl(key)

                if ttl < 1800 and ttl not in (-1, -2):  # Меньше 30 минут и не истекший
                    value = await self.get_data(key=key, use_json=True)
                    if not isinstance(value, list):
                        value = [value]

                    user_keys.setdefault(user_id, []).append(key)
                    user_id_to_message_id.setdefault(user_id, []).extend(value)
        return user_keys, user_id_to_message_id

    async def _delete_keys_for_users_without_active_keys(self, users_with_expired_keys, user_id_to_message_id):
        users_to_cleaning = []
        messages_to_delete = dict()
        for user_id, keys in users_with_expired_keys.items():
            if await self._has_active_keys(user_id):
                continue
            for key in keys:
                await self.redis_base.delete(key)
            users_to_cleaning.append(user_id)
            messages_to_delete[user_id] = user_id_to_message_id[user_id]

        return messages_to_delete

    async def _scan_keys(self, pattern):
        cursor = 0
        while True:
            cursor, keys = await self.redis_base.scan(cursor, match=pattern, count=100)
            for key in keys:
                yield key
            if cursor == 0:
                break

    async def _has_active_keys(self, user_id):
        async for key in self._scan_keys(f'{user_id}:*'):
            ttl = await self.redis_base.ttl(key)

            if 0 <= ttl >= 1800:  # Еще активный или без ttl

                return True


        return False
    async def getset_data(self, key, value):
        try:
            if type(value) not in (int, float, str):
                value = value
                value = json.dumps(value)

            await self.redis_base.getset(key, value)
            value_is_set = await self.redis_base.get(key) == value
            if value_is_set:
                print('good', {key: value})
                return True
            else:
                print('error', {key: value})
                return False
        except ConnectionError as ex:
            traceback.print_exc()
            await asyncio.sleep(1)
            await redis_data.getset_data(key, value)


    async def set_data(self, key: str = None,
                       value: Union[set, list, str, float, dict] = None,
                       dicted_data: dict = None, expire=None) -> bool:

        expire = await self.set_ttl(key, expire)
        try:
            if dicted_data:
                for key, value in dicted_data.items():
                    if type(value) not in (int, float, str):
                        value = await value
                        value = json.dumps(value)

                    await self.redis_base.set(key, value)
                    value_is_set = await self.redis_base.get(key) == value
                    if value_is_set:
                        print('good', {key: value})
                        if expire:
                            await self.redis_base.expire(key, expire)
                        pass
                    else:
                        print('error', {key: value})
                        return False


            else:
                if type(value) not in (int, float, str):
                    value = json.dumps(value)
                #выдаёт false если числовое value(становится стр)
                await self.redis_base.set(key, value)

                if isinstance(value, int):
                    value_is_set = await self.redis_base.get(key) == str(value)
                else:
                    value_is_set = await self.redis_base.get(key) == value
                if value_is_set:
                    print('good', {key: value})
                    if expire:
                        await self.redis_base.expire(key, expire)
                    return True
                else:
                    print('error', {key: value})
                    return False
        except ConnectionError as ex:
            traceback.print_exc()
            await asyncio.sleep(1)
            return await redis_data.set_data(key, value, dicted_data, expire)

    async def get_data(self, key: str, use_json=False) -> Union[bool, Union[set, list, str, float, dict]]:
        try:
            result = await self.redis_base.get(key)
            print('redisult-get type', type(result))
            if use_json and result:
                result = json.loads(result)

            if result:
                print('good_get', {key: result})
                return result
            else:
                print('error_get', key)
                return False
        except ConnectionError as ex:
            traceback.print_exc()
            await asyncio.sleep(1)
            return await redis_data.get_data(key, use_json)

    async def delete_key(self, key: str):
        try:
            # Удаляем ключ
            result = await self.redis_base.delete(key)
            if result == 1:
                print(f"Ключ '{key}' успешно удален")
                return True
            else:
                print(f"Ключ '{key}' не найден")
                return False

        except ConnectionError as ex:
            traceback.print_exc()
            await asyncio.sleep(1)
            await redis_data.delete_key(key)

    async def set_ttl(self, key, expire):
        if not expire:
            if any(sub_key in key for sub_key in self.keys_storage['messages']):
                expire = 48 * 60 * 60
                return expire

redis_data = RedisRequester()