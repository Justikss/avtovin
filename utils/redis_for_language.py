import json
from typing import Union

from redis import asyncio as aioredis




class RedisRequester:
    def __init__(self):
        self.redis_base = aioredis.StrictRedis(
            host='localhost',
            decode_responses=True
        )

    async def set_data(self, key: str = None,
                       value: Union[set, list, str, float, dict] = None,
                       dicted_data: dict = None) -> bool:
        if dicted_data:
            for key, value in dicted_data.items():
                if type(value) not in (int, float, str):
                    value = await value
                    value = json.dumps(value)

                await self.redis_base.set(key, value)
                value_is_set = await self.redis_base.get(key) == value
                if value_is_set:
                    print('good', {key: value})
                    pass
                else:
                    print('error', {key: value})
                    await self.redis_base.close()
                    return False

            await self.redis_base.close()

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
                await self.redis_base.close()
                print('good', {key: value})
                return True
            else:
                await self.redis_base.close()
                print('error', {key: value})
                return False

    async def get_data(self, key: str, use_json=False) -> Union[bool, Union[set, list, str, float, dict]]:
        result = await self.redis_base.get(key)
        print('redisult-get type', type(result))
        if use_json and result:
            result = json.loads(result)

        if result:
            await self.redis_base.close()
            print('good_get', {key: result})
            return result
        else:
            await self.redis_base.close()
            print('error_get', key)
            return False

    async def delete_key(self, key: str):
        # Удаляем ключ
        result = await self.redis_base.delete(key)
        if result == 1:
            print(f"Ключ '{key}' успешно удален")
            return True
        else:
            print(f"Ключ '{key}' не найден")
            return False

        # Закрываем соединение
        await self.redis_base.close()


redis_data = RedisRequester()