import asyncio
import importlib
from copy import copy
from typing import Callable, Dict, Any, Awaitable

from aiogram import Bot, BaseMiddleware
from aiogram.types import CallbackQuery, Message
from datetime import datetime, timedelta
import time

from handlers.custom_filters.throttling import delete_message
from config_data.config import spam_block_time, anti_spam_duration
from keyboards.reply.send_reply_markup import send_reply_button_contact

lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1, long_term_spam_count: int = 5, long_term_duration: int = 7,
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

        current_time = time.time()
        if not await self.check_rate_limit(user_id, current_time):
            return  # Слишком быстрое действие, пропускаем обработку

        # Проверка долгосрочного спама и блокировка пользователя при необходимости
        if not await self.check_long_term_spam(user_id, event.bot):
            await self.notify_user(bot, user_id)
            return

        lock = await self.acquire_lock(user_id)
        if lock.locked():
            return False

        async with lock:
            header_controller_module = importlib.import_module('handlers.default_handlers.start')
            await asyncio.sleep(anti_spam_duration)
            print('MWAREHEADER')
            if await self.chat_header_controller_support(event):
                await header_controller_module.header_controller(event)

            await handler(event, data)
            ic('UNLOK')
            return

    async def chat_header_controller_support(self, event):
        if isinstance(event, CallbackQuery):
            if event.data in ('backward:user_registration_number', 'backward:seller_registration_number'):
                from keyboards.reply.delete_reply_markup import delete_reply_markup
                await delete_reply_markup(event)
                return False
            elif event.data == 'rewrite_seller_number':
                await send_reply_button_contact(event)
                return False

        return True
    async def send_notification(self, bot: Bot, user_id: int, message: str, timer: int):
        last_text_to_send = None
        text = f'<blockquote><b>{copy(message)}</b></blockquote>'


        # await delete_message(bot, user_id, notification_message)
        alert_message = await bot.send_message(chat_id=user_id, text=text)
        ic()
        # for time_point in range(timer + 1, 0, -1):
        #     if '{time}' in text:
        #         text_to_send = text.format(time=time_point)
        #     else:
        #         text_to_send = text + str(time_point)
        #     if last_text_to_send != text_to_send:
        #         await alert_message.edit_text(text=text_to_send)
        #         last_text_to_send = text_to_send

        await asyncio.sleep(timer)
        await delete_message(bot, user_id, alert_message.message_id)

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
                # await delete_message(bot, user_id, block_info['message'])
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
                ic()
                await self.send_notification(bot, user_id, lexicon_module.LEXICON['callback_spam_detected'], self.block_duration)
                return False
        else:
            long_term_data['count'] = 1
            long_term_data['time'] = datetime.now()
        return True

    async def acquire_lock(self, user_id: int):
        ic(self.locks, user_id, user_id not in self.locks)
        if user_id not in self.locks:
            self.locks[user_id] = asyncio.Lock()
        return self.locks[user_id]

#
# asyncioaa = asyncio.Lock()
# asyncioaa.locked()

