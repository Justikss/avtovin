import asyncio
import importlib
from copy import copy
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_data.config import spam_block_time, message_answer_awaited, anti_spam_duration

# Глобальные переменные
global_locks = {}
global_user_message_counts = {}
global_blocked_users = {}
global_active_notifications = {}

long_term_spam_count = 8  # Пример: 8 сообщений
long_term_duration = 3600  # Пример: 1 час (3600 секунд)
global_long_term_user_message_counts = {}
lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


async def delete_message(bot, chat_id, message_id):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except TelegramBadRequest:
        pass

async def notify_user(bot: Bot, user_id: int, message: str, timer: int, mode: str):
    last_text_to_send = None
    text = f'<blockquote><b>{copy(message)}</b></blockquote>'

    await asyncio.sleep(anti_spam_duration)
    alert_message = await bot.send_message(chat_id=user_id, text=text)

    for time_point in range(timer + 1, 0, -1):
        if '{time}' in text:
            text_to_send = text.format(time=time_point)
        else:
            text_to_send = text + str(time_point)
        if last_text_to_send != text_to_send:
            await alert_message.edit_text(text=text_to_send)
            last_text_to_send = text_to_send

        await asyncio.sleep(1)
    await delete_message(bot, user_id, alert_message.message_id)
    del global_blocked_users[user_id]
    match mode:
        case 'long':
            del global_long_term_user_message_counts[user_id]
        case 'default':
            del global_user_message_counts[user_id]

async def check_blocked_users(bot):
    while True:
        current_time = datetime.now()
        for user_id, block_time in list(global_blocked_users.items()):
            if current_time >= block_time:
                del global_blocked_users[user_id]
                # Здесь должен быть код для отправки уведомления пользователю
                await notify_user(bot, user_id, lexicon_module.LEXICON['spam_passed'],
                                  message_answer_awaited, 'end')

        await asyncio.sleep(10)

# Запуск глобальной задачи

class ThrottlingFilter(BaseFilter):
    rate_limit = 0.5
    spam_detection_count = 4
    block_duration = spam_block_time

    async def __call__(self, message: Message, handler):
        user_id = message.from_user.id

        # Проверка блокировки пользователя
        if user_id in global_blocked_users:
            if datetime.now() >= global_blocked_users[user_id]:
                # Время блокировки истекло, разрешаем пользователю отправлять сообщения
                del global_blocked_users[user_id]
            else:
                # Пользователь всё ещё заблокирован
                await delete_message(message.bot, user_id, message.message_id)
                return False

        # Обновление или инициализация блокировки
        lock = global_locks.setdefault(user_id, asyncio.Lock())
        if lock.locked():
            try:
                await message.delete()
            except TelegramBadRequest:
                pass
            return False

        long_term_count_data = global_long_term_user_message_counts.setdefault(
            user_id, {'count': 0, 'time': datetime.now()}
        )
        if datetime.now() - long_term_count_data['time'] <= timedelta(seconds=long_term_duration):
            long_term_count_data['count'] += 1
            if long_term_count_data['count'] >= long_term_spam_count:
                # Пользователь считается спамером в длительном интервале
                ic('ПОПАЛСЯ')
                global_blocked_users[user_id] = datetime.now() + timedelta(seconds=self.block_duration)
                await notify_user(message.bot, user_id=user_id,
                                  message=lexicon_module.LEXICON['spam_detected'],
                                  timer=self.block_duration, mode='long')
                return False
        else:
            long_term_count_data['count'] = 1
            long_term_count_data['time'] = datetime.now()

        global_user_message_counts.setdefault(user_id, {'count': 0, 'time': datetime.now()})
        user_message_count = global_user_message_counts[user_id]

        if datetime.now() - user_message_count['time'] <= timedelta(seconds=self.block_duration):
            user_message_count['count'] += 1
            if user_message_count['count'] >= self.spam_detection_count:
                global_blocked_users[user_id] = datetime.now() + timedelta(seconds=self.block_duration)
                # Здесь должен быть код для отправки уведомления пользователю
                global_blocked_users[user_id] = datetime.now() + timedelta(seconds=self.block_duration)
                await notify_user(message.bot, user_id=user_id,
                                               message=lexicon_module.LEXICON['spam_detected'],
                                               timer=self.block_duration, mode='default')
                return False
        else:
            user_message_count['count'] = 1
            user_message_count['time'] = datetime.now()

        lock = global_locks.setdefault(user_id, asyncio.Lock())
        async with lock:
            await asyncio.sleep(anti_spam_duration)
            return True

# Пример подключения фильтра
# dp.filters_factory.bind(ThrottlingFilter)
