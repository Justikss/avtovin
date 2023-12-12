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

redis_data = RedisRequester()