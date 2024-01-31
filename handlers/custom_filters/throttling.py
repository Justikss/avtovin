import asyncio
import importlib
from copy import copy
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from config_data.config import spam_block_time, message_answer_awaited, anti_spam_duration, long_term_spam_block_time

# Глобальные переменные
global_locks = {}
global_user_message_counts = {}
global_blocked_users = {}
global_active_notifications = {}

long_term_spam_count = 15  # сообщений
long_term_duration = 60  # время
global_long_term_user_message_counts = {}
lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


async def delete_message(bot, chat_id, message_id):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except TelegramBadRequest:
        pass

class ThrottlingFilter(BaseFilter):
    rate_limit = 1.4
    spam_detection_count = 2
    block_duration = spam_block_time
    long_term_spam_block_time = long_term_spam_block_time

    async def __call__(self, message: Message, state: FSMContext, handler):
        global global_locks, global_user_message_counts, global_blocked_users, global_active_notifications, \
            long_term_spam_count, long_term_duration, global_long_term_user_message_counts
        user_id = message.from_user.id
        ic(handler)

        # Проверка блокировки пользователя
        ic(user_id in global_blocked_users)
        if user_id in global_blocked_users:
            ic(datetime.now() >= global_blocked_users[user_id])
            if datetime.now() >= global_blocked_users[user_id]:
                # Время блокировки истекло, разрешаем пользователю отправлять сообщения
                del global_blocked_users[user_id]
            else:
                # Пользователь всё ещё заблокирован
                # await delete_message(message.bot, user_id, message.message_id)
                return False
        ic()
        ic(user_id in global_blocked_users)
        if user_id in global_blocked_users:
            ic(datetime.now() >= global_blocked_users[user_id])
        # Обновление или инициализация блокировки
        lock = global_locks.setdefault(user_id, asyncio.Lock())
        if lock.locked():
            await delete_message(bot=message.bot, message_id=message.message_id, chat_id=message.chat.id)
            return False

        long_term_count_data = global_long_term_user_message_counts.setdefault(
            user_id, {'count': 0, 'time': datetime.now()}
        )
        if datetime.now() - long_term_count_data['time'] <= timedelta(seconds=long_term_duration):
            long_term_count_data['count'] += 1
            if long_term_count_data['count'] >= long_term_spam_count:
                # Пользователь считается спамером в длительном интервале
                ic('ПОПАЛСЯ')
                global_blocked_users[user_id] = datetime.now() + timedelta(seconds=self.long_term_spam_block_time)
                await self.notify_user(message.bot, user_id=user_id,
                                  message=lexicon_module.LEXICON['spam_detected'],
                                  timer=self.long_term_spam_block_time, mode='long')
                return False
        else:
            long_term_count_data['count'] = 1
            long_term_count_data['time'] = datetime.now()

        global_user_message_counts.setdefault(user_id, {'count': 0, 'time': datetime.now()})
        user_message_count = global_user_message_counts[user_id]

        if datetime.now() - user_message_count['time'] <= timedelta(seconds=self.rate_limit):
            user_message_count['count'] += 1
            if user_message_count['count'] >= self.spam_detection_count:
                global_blocked_users[user_id] = datetime.now() + timedelta(seconds=self.block_duration)
                # Здесь должен быть код для отправки уведомления пользователю
                ic('ПОПАЛСЯ 2')

                global_blocked_users[user_id] = datetime.now() + timedelta(seconds=self.block_duration)
                await self.notify_user(message.bot, user_id=user_id,
                                               message=lexicon_module.LEXICON['spam_detected'],
                                               timer=self.block_duration, mode='default')
                return False
        else:
            user_message_count['count'] = 1
            user_message_count['time'] = datetime.now()

        lock = await self.acquire_lock(user_id)
        if lock.locked():
            return False

        async with lock:
            await asyncio.sleep(anti_spam_duration)
            return True

    async def acquire_lock(self, user_id: int):
        ic(global_locks, user_id, user_id not in global_locks)
        if user_id not in global_locks:
            global_locks[user_id] = asyncio.Lock()
        return global_locks[user_id]

    async def notify_user(self, bot: Bot, user_id: int, message: str, timer: int, mode: str):
        lock = await self.acquire_lock(user_id)
        if lock.locked():
            return
        async with lock:
            timer -= 1
            last_text_to_send = None
            text = f'<blockquote><b>{copy(message)}</b></blockquote>'

            await asyncio.sleep(anti_spam_duration)
            alert_message = await bot.send_message(chat_id=user_id, text=text.format(time=timer))

            # for time_point in range(timer + 1, 0, -1):
            #     if '{time}' in text:
            #         text_to_send = text.format(time=time_point)
            #     else:
            #         text_to_send = text + str(time_point)
            #     if last_text_to_send != text_to_send:
            #         await alert_message.edit_text(text=text_to_send)
            #         last_text_to_send = text_to_send

            await asyncio.sleep(timer)
            ic()
            await delete_message(bot, user_id, alert_message.message_id)
            if global_blocked_users.get(user_id):
                del global_blocked_users[user_id]
            match mode:
                case 'long':
                    del global_long_term_user_message_counts[user_id]
                case 'default':
                    del global_user_message_counts[user_id]

# Пример подключения фильтра
# dp.filters_factory.bind(ThrottlingFilter)
