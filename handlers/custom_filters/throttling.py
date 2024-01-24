import asyncio

from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter
from aiogram.types import Message

class ThrottlingFilter(BaseFilter):
    def __init__(self, rate_limit: float = 0.4):
        self.rate_limit = rate_limit
        self.locks = {}

    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id

        if user_id not in self.locks:
            self.locks[user_id] = asyncio.Lock()

        lock = self.locks[user_id]

        if lock.locked():
            try:
                await message.delete()
            except TelegramBadRequest:
                pass
            return False  # Это сообщение будет отклонено обработчиком

        async with lock:
            await asyncio.sleep(self.rate_limit)  # Устанавливаем задержку обработки
            return True

# Для использования этого фильтра его нужно зарегистрировать и применить к обработчикам
# dp.filters_factory.bind(ThrottlingFilter, event_handlers=[dp.message_handlers])
# Затем можно использовать его в декораторах обработчиков
# @dp.message_handler(throttling_filter=1.0)
