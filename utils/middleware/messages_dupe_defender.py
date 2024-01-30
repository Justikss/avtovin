import asyncio
import importlib
import logging
from copy import copy
from datetime import datetime, timedelta
from aiogram import BaseMiddleware, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from typing import Callable, Any, Dict, Awaitable

from config_data.config import spam_block_time, message_answer_awaited

lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

class MessageThrottlingMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, rate_limit: float = 3.0, spam_detection_count: int = 4, block_duration: int = spam_block_time):
        super().__init__()
        self.bot = bot
        self.rate_limit = rate_limit
        self.spam_detection_count = spam_detection_count
        self.block_duration = block_duration  # Время блокировки в секундах
        self.locks = {}
        self.user_message_counts = {}
        self.blocked_users = {}
        asyncio.create_task(self.check_blocked_users())

    async def check_blocked_users(self):
        while True:
            current_time = datetime.now()
            for user_id, block_time in list(self.blocked_users.items()):
                if current_time >= block_time:
                    del self.blocked_users[user_id]
                    # Отправляем сообщение пользователю о снятии блокировки
                    await self.notify_user(user_id, lexicon_module.LEXICON['spam_passed'], message_answer_awaited)
            await asyncio.sleep(10)  # Проверяем каждые 10 секунд

    async def notify_user(self, user_id: int, message: str, timer: int):
        pass
        if timer > 2:
            timer -= 1
        last_text_to_send = None
        text = f'<blockquote><b>{copy(message)}</b></blockquote>'
        alert_message = await self.bot.send_message(chat_id=user_id, text=text)
        for time_point in range(timer+1, 0, -1):
            if '{time}' in text:
                text_to_send = text.format(time=time_point)
            else:
                text_to_send = text + str(time_point)
            if last_text_to_send != text_to_send:
                await alert_message.edit_text(text=text_to_send)
                last_text_to_send = text_to_send

            await asyncio.sleep(1)

        try:
            await self.bot.delete_message(chat_id=user_id, message_id=alert_message.message_id)
        except TelegramBadRequest:
            pass


    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        if user_id in self.blocked_users:
            return False  # Пользователь заблокирован, игнорируем сообщение

        if any((event.audio, event.photo, event.video, event.document)):
            return await handler(event, data)

        self.user_message_counts.setdefault(user_id, {'count': 0, 'time': datetime.now()})
        user_message_count = self.user_message_counts[user_id]

        if datetime.now() - user_message_count['time'] <= timedelta(seconds=self.block_duration):
            user_message_count['count'] += 1
            if user_message_count['count'] >= self.spam_detection_count:
                # # Блокируем пользователя и уведомляем его
                # self.blocked_users[user_id] = datetime.now() + timedelta(seconds=self.block_duration)
                # await self.notify_user(user_id=user_id,
                #                        message=lexicon_module.LEXICON['spam_detected'],
                #                        timer=self.block_duration)
                return False
        else:
            user_message_count['count'] = 1
            user_message_count['time'] = datetime.now()

        lock = self.locks.setdefault(user_id, asyncio.Lock())
        async with lock:
            await asyncio.sleep(self.rate_limit)
            await handler(event, data)


# Пример подключения мидлвэари
# bot = Bot(token="YOUR_TOKEN")
# dp = Dispatcher(bot)
# dp.middleware.setup(MessageThrottlingMiddleware())
