from aiogram.types import Message


async def del_cached_configs(message: Message):
    from utils.redis_for_language import cache_redis
    from utils.redis_for_language import redis_data
    l = [n async for n in redis_data._scan_keys('cached_car_config*')]
    if l:
        await redis_data.redis_base.delete(*l)
        if l:
            text = 'yes'
        else:
            text = 'no'

        await message.answer(text)
    else:
        await message.answer('empty')
