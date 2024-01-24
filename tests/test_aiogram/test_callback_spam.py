import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery, User
import pytest
from datetime import datetime

# Ваш мидлвэри
import asyncio
import importlib
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
import time
from typing import Callable, Any, Dict, Awaitable

from icecream import ic

from tests.test_aiogram.utils import get_callback, get_update

# ic.disable()

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
        # ic()
        # Создание блокировки для пользователя, если еще нет
        if user_id not in self.locks:
#             ic()
            self.locks[user_id] = asyncio.Lock()

        async with self.locks[user_id]:  # Блокировка на время обработки запроса
            if user_id in self.last_action:
                time_since_last_action = current_time - self.last_action[user_id]
                if time_since_last_action < self.rate_limit:
                    # Пропуск обработки запроса, если запросы слишком частые
                    return

            self.last_action[user_id] = current_time
            # ic(handler)
            return await handler(event, data)

handler_called = False
# Тестовая функция
@pytest.mark.asyncio
async def test_throttling_middleware(dispatcher: Dispatcher, bot):
    dp = dispatcher
    dp.callback_query.middleware(ThrottlingMiddleware())

    global handler_called
    handler_called = False

    @dp.callback_query(lambda c: True)
    async def callback_handler(callback_query: CallbackQuery):
        global handler_called
        handler_called = True
        await callback_query.answer()

    interval = 0.05  # Начальный интервал
    successful_processes = 0
    max_attempts = 5
    attempts = 0

    while successful_processes < 2 and attempts < max_attempts:
        handler_called = False
        await asyncio.sleep(interval)
        await dp._process_update(bot=bot, update=get_update(callback=get_callback('test_data')))

        # Проверка, что предыдущий обработчик завершил свою работу
        ic(dp.callback_query.middleware[-1].locks)
        user_lock = dp.callback_query.middleware[-1].locks.get(123)
        if user_lock and not user_lock.locked():
            if handler_called:
                successful_processes += 1
            else:
                successful_processes = 0
        else:
            successful_processes = 0

        interval += 0.05
        attempts += 1
    if attempts != max_attempts and successful_processes == 2:
        print(f"\nМинимальный интервал для двух успешных обработок подряд: {interval}")
    else:
        print(f'\nНеудачно. Попыток {attempts} из {max_attempts}. \nУспешных процессов подряд - {successful_processes}',
              file=sys.stderr)

