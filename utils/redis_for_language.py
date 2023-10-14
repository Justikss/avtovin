from typing import Union

import redis


class RedisRequester:
    def __init__(self):
        self.redis_base = redis.StrictRedis(
            host='localhost',
            charset="utf-8",
            decode_responses=True
        )

    async def set_data(self, key: str,
                       value: Union[set, list, str, float, dict]) -> bool:
        '''Ассинхронный метод устанавливает значение языковому ключу в Redis
        Даёт обратную связь
        :rtype: bool
        :key[str]: Ключ для записи в базу Redis
        :value[Union[set, list, str, float, dict]]: значение для записи в базу Redis'''
        self.redis_base.set(key, value)
        if self.redis_base.get(key) == value:
            return True
        else:
            return False

        redis_base.close()

    async def get_data(self, key: str) -> Union[bool, Union[set, list, str, float, dict]]:
        '''Ассинхронный метод выдаёт значение по входящему ключу в Redis
        Даёт обратную связь
        :return: False | result
        :rtype: Union[bool, Union[set, list, str, float, dict]]
        :key: Ключ для записи в базу Redis
        '''
        result = self.redis_base.get(key)
        if result:
            return result
        else:
            return False

        redis_base.close()


redis_data = RedisRequester()
