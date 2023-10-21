import json
from typing import Union

import redis
import aioredis


class RedisRequester:
    def __init__(self):
        self.redis_base = redis.StrictRedis(
            host='localhost',
            charset="utf-8",
            decode_responses=True
        )

    async def set_data(self, key: str = None,
                       value: Union[set, list, str, float, dict] = None,
                       dicted_data: dict = None) -> bool:
        '''Ассинхронный метод устанавливает значение языковому ключу в Redis
        Даёт обратную связь
        :rtype: bool
        :key[str]: Ключ для записи в базу Redis
        :value[Union[set, list, str, float, dict]]: значение для записи в базу Redis'''
        if dicted_data:
            for key, value in dicted_data.items():
                if type(value) not in (int, float, str):

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

            self.redis_base.close()

        else:
            if type(value) not in (int, float, str):
                value = json.dumps(value)

            await self.redis_base.set(key, value)
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
        '''Ассинхронный метод выдаёт значение по входящему ключу в Redis
        Даёт обратную связь
        :return: False | result
        :rtype: Union[bool, Union[set, list, str, float, dict]]
        :key: Ключ для записи в базу Redis
        '''
        result = self.redis_base.get(key)
        print('redisult type', type(result))
        if use_json:
            result = json.loads(result)

        if result:
            self.redis_base.close()
            print('good_get', {key: result})
            return result
        else:
            self.redis_base.close()
            print('error_get', key)
            return False




redis_data = RedisRequester()
