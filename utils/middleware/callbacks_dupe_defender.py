import asyncio
import importlib
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
import time
from typing import Callable, Any, Dict, Awaitable

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1):
        super().__init__()
        self.rate_limit = rate_limit
        self.last_action = {}
        self.locks = {}

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery | Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()

        # Создание блокировки для пользователя, если еще нет
        if user_id not in self.locks:
            self.locks[user_id] = asyncio.Lock()

        async with self.locks[user_id]:  # Блокировка на время обработки запроса
            if user_id in self.last_action:
                time_since_last_action = current_time - self.last_action[user_id]
                if time_since_last_action < self.rate_limit:
                    # Пропуск обработки запроса, если запросы слишком частые
                    return

            self.last_action[user_id] = current_time
            header_controller_module = importlib.import_module('handlers.default_handlers.start')
            await header_controller_module.header_controller(event)
            return await handler(event, data)
