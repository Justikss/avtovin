import asyncio
import importlib
from typing import Callable, Dict, Any, Awaitable

from aiogram import Bot, BaseMiddleware
from aiogram.types import CallbackQuery, Message
from datetime import datetime, timedelta
import time

from config_data.config import spam_block_time


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1, long_term_spam_count: int = 2, long_term_duration: int = 3600,
                 block_duration: int = spam_block_time):
        super().__init__()
        self.rate_limit = rate_limit
        self.long_term_spam_count = long_term_spam_count
        self.long_term_duration = long_term_duration
        self.block_duration = block_duration  # Время блокировки в секундах
        self.last_action = {}
        self.long_term_activity = {}
        self.user_block_time = {}
        self.locks = {}

    async def notify_user(self, bot: Bot, user_id: int):
        # Проверка, истекло ли время блокировки
        if user_id in self.user_block_time:
            block_info = self.user_block_time[user_id]
            if datetime.now() < block_info['end_time']:
                # Блокировка все еще активна, не отправляем новое уведомление
                return
            else:
                # Удаляем информацию о блокировке, если она истекла
                del self.user_block_time[user_id]
                del self.long_term_activity[user_id]
    async def check_user_block(self, user_id: int, bot: Bot) -> bool:
        ic(user_id in self.user_block_time)
        ic(self.user_block_time)
        if user_id in self.user_block_time:
            block_info = self.user_block_time[user_id]
            ic(block_info['end_time'])
            now = datetime.now()
            if now < block_info['end_time']:
                print(
                    f"User {user_id} is still blocked until {block_info['end_time']} (now: {now})")  # Добавлено логгирование
                return False
            else:
                try:
                    await bot.delete_message(user_id, block_info['message'])
                except Exception as e:
                    print(f"Error deleting block message: {e}")  # Логгирование ошибки
                #отключаем ограничения по истечению времени
                del self.user_block_time[user_id]
                del self.long_term_activity[user_id]
                print(f"Block for user {user_id} has been lifted")  # Добавлено логгирование
        return True

    async def check_rate_limit(self, user_id: int, current_time: float) -> bool:
        if user_id in self.last_action:
            time_since_last_action = current_time - self.last_action[user_id]
            if time_since_last_action < self.rate_limit:
                return False
        self.last_action[user_id] = current_time
        return True

    async def check_long_term_spam(self, user_id: int, bot: Bot) -> bool:
        ic(self.long_term_activity)
        if user_id not in self.long_term_activity:
            self.long_term_activity[user_id] = {'count': 0, 'time': datetime.now()}

        # Проверка, не заблокирован ли пользователь уже по другим причинам
        if user_id in self.user_block_time and datetime.now() < self.user_block_time[user_id]['end_time']:
            return False

        long_term_data = self.long_term_activity[user_id]
        if datetime.now() - long_term_data['time'] <= timedelta(seconds=self.long_term_duration):
            long_term_data['count'] += 1
            if long_term_data['count'] >= self.long_term_spam_count:
                self.user_block_time[user_id] = {'start_time': datetime.now(),
                                                 'end_time': datetime.now() + timedelta(seconds=self.block_duration)}
                await bot.send_message(user_id,
                                       "Вы отправляете сообщения слишком часто. Пожалуйста, снизьте активность.")
                return False
        else:
            long_term_data['count'] = 1
            long_term_data['time'] = datetime.now()
        return True

    async def acquire_lock(self, user_id: int):
        if user_id not in self.locks:
            self.locks[user_id] = asyncio.Lock()
        return self.locks[user_id]

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery | Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        bot = data.get('bot', None)

        if not await self.check_user_block(user_id, bot):
            return  # Пользователь заблокирован, прекращаем обработку

        # Проверка долгосрочного спама и блокировка пользователя при необходимости
        if not await self.check_long_term_spam(user_id, event.bot):
            await self.notify_user(bot, user_id)
            return

        lock = await self.acquire_lock(user_id)
        async with lock:
            if not await self.check_rate_limit(user_id, time.time()):
                return

            header_controller_module = importlib.import_module('handlers.default_handlers.start')
            await header_controller_module.header_controller(event)
            return await handler(event, data)