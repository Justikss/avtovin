import asyncio
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Any, Dict, Awaitable

class MessageThrottlingMiddleware(BaseMiddleware):
    def __init__(self, additional_processing_time: float = 15000.0):
        super().__init__()
        self.additional_processing_time = additional_processing_time
        self.locks = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        if user_id not in self.locks:
            self.locks[user_id] = asyncio.Lock()

        lock = self.locks[user_id]
        ic(self.locks)
        if ic(lock.locked()):
            try:
                await event.delete()
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
            return

        async with lock:
            await handler(event, data)
            # Добавляем дополнительное время к блокировке
            # await asyncio.sleep(self.additional_processing_time)

# Пример подключения мидлвэари
# bot = Bot(token="YOUR_TOKEN")
# dp = Dispatcher(bot)
# dp.middleware.setup(MessageThrottlingMiddleware(additional_processing_time=150.0))
