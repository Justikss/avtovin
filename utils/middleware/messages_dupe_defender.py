import asyncio
from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from typing import Callable, Any, Dict, Awaitable

class MessageThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 0.4):
        super().__init__()
        self.rate_limit = rate_limit
        self.locks = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        if any((event.audio, event.photo, event.video, event.document)):
            return await handler(event, data)


        if user_id not in self.locks:
            self.locks[user_id] = asyncio.Lock()

        lock = self.locks[user_id]

        if lock.locked():
            from handlers.utils.delete_message import delete_message
            await delete_message(event, event.message_id)
            return False  # Это сообщение будет отклонено обработчиком

        async with lock:
            await asyncio.sleep(self.rate_limit)  # Устанавливаем задержку обработки
            await handler(event, data)

        # async with lock:

            # Добавляем дополнительное время к блокировке
            # await asyncio.sleep(self.additional_processing_time)

# Пример подключения мидлвэари
# bot = Bot(token="YOUR_TOKEN")
# dp = Dispatcher(bot)
# dp.middleware.setup(MessageThrottlingMiddleware(additional_processing_time=150.0))
