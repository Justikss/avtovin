import asyncio
import importlib
import traceback
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import CallbackQuery, Message, Update
from datetime import datetime, timedelta

from config_data.config import spam_block_time, anti_spam_duration, long_term_spam_block_time, DEVELOPER_TELEGRAM_ID
from keyboards.reply.send_reply_markup import send_reply_button_contact
from utils.middleware.update_spam_defender.modules.callback import CallbackSpamDefender
from utils.middleware.update_spam_defender.modules.errors import ErrorHandler
from utils.middleware.update_spam_defender.modules.language import LanguageMiddlewareModule
from utils.middleware.update_spam_defender.modules.media_groups_cleaner import CleanerModule
from utils.middleware.update_spam_defender.modules.message import MessageSpamDefender

lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
header_controller_module = importlib.import_module('handlers.default_handlers.start')

# Глобальные переменные для отслеживания активности пользователей
global_user_message_counts = {}
global_blocked_users = {}
global_long_term_user_message_counts = {}

redis_module = importlib.import_module('utils.redis_for_language')
redis_get = redis_module.redis_data.get_data
redis_set = redis_module.redis_data.set_data

class UpdateThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.4, spam_detection_count: int = 2, long_term_spam_count: int = 15,
                 long_term_duration: int = 60):
        super().__init__()
        self.rate_limit = rate_limit
        self.spam_detection_count = spam_detection_count
        self.long_term_spam_count = long_term_spam_count
        self.long_term_duration = long_term_duration
        self.block_duration = spam_block_time  # Время блокировки в секундах
        self.long_term_block_duration = long_term_spam_block_time  # Длительное время блокировки
        self.locks = {}

        self.callback_spam_handler = CallbackSpamDefender()
        self.message_spam_defender = MessageSpamDefender()
        self.language_handler = LanguageMiddlewareModule()
        self.cleaner_module = CleanerModule()
        self.error_handler = ErrorHandler()

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        message = event.message
        callback = event.callback_query
        ic(data)
        if callback:
            request = callback
            message = request.message
        else:
            request = message
            message = request

        if message.chat.type != ChatType.PRIVATE:
            return





        if isinstance(request, Message):
            if any((message.photo, message.video, message.audio, message.document)):
                return await handler(event, data)
            bot = message.bot
            success_filtration = await self.message_spam_defender(request, data.get('state'))
        else:
            bot = event.callback_query.bot
            success_filtration = await self.callback_spam_handler(callback, bot)

        if not success_filtration:
            return



        data['bot'] = bot
        user_id = self.get_user_id(request)
        if not user_id:
            return

        lock = self.locks.get(user_id)

        if lock is None:
            # Если блокировка не найдена, создаем новую и сохраняем ее
            lock = asyncio.Lock()
            self.locks[user_id] = lock

        # Проверяем, заблокирован ли пользователь
        if lock.locked():
            # Если заблокирован, игнорируем этот апдейт
            return

        async with lock:
            # Обработка апдейта, если блокировка свободна
            await self.language_handler(request)

            await self.cleaner_module(request)
            await asyncio.sleep(anti_spam_duration)


            try:
                ic(user_id, DEVELOPER_TELEGRAM_ID, user_id != DEVELOPER_TELEGRAM_ID)
                if await redis_get('develop_moment_flag') and user_id != int(DEVELOPER_TELEGRAM_ID):
                    await self.handle_develop_moment(request, message)
                else:
                    if ic(await self.chat_header_controller_support(request, data.get('state'))):
                        await asyncio.sleep(anti_spam_duration)

                        await header_controller_module.header_controller(request)
                    return await handler(event, data)
            except TelegramForbiddenError as exception:
                await self.error_handler(request, exception)
            except Exception as exception:
                await self.error_handler.logging_exception(exception, request)
                pass
            finally:
                if isinstance(request, CallbackQuery):
                    await request.answer()
    async def handle_develop_moment(self, request, message):
        user_id = request.from_user.id
        personal_redis_key = f'{user_id}:sended_develop_moment_info'

        if not await redis_get(personal_redis_key):
            notification_message = await message.bot.send_message(chat_id=message.chat.id,
                                                                  text=lexicon_module.LEXICON[
                                                                      'develop_moment_notif'])
            await redis_set(personal_redis_key, notification_message.message_id)
    async def chat_header_controller_support(self, event, state):
        # return True
        ic(str(await state.get_state()) == 'CarDealerShipRegistrationStates:input_dealship_name')
        current_state = str(await state.get_state())
        ic(str(await state.get_state()))
        if isinstance(event, CallbackQuery):
            ic(event.data)
        if isinstance(event, CallbackQuery):
            if event.data == 'rewrite_seller_name':
                await header_controller_module.header_controller(event, True)
            elif event.data == 'confirm_registration_from_seller':
                await header_controller_module.header_controller(event)


                return False
        if current_state == 'CarDealerShipRegistrationStates:input_dealship_name':
            if isinstance(event, CallbackQuery) and event.data.startswith('backward:'):
                # from keyboards.reply.delete_reply_markup import delete_reply_markup
                # await delete_reply_markup(event)
                pass
            else:
                return False
        elif current_state in ('HybridSellerRegistrationStates:check_input_data') and isinstance(event, CallbackQuery) and event.data.startswith('backward'):
            ic()
            return False
        elif current_state == 'BuyerRegistationStates:finish_check_phone_number':
            if isinstance(event, CallbackQuery) and event.data.startswith('backward'):
                return True
            return False
        ic(isinstance(event, Message) and event.text == '/start')
        if isinstance(event, CallbackQuery):
            # if event.data in ('backward:user_registration_number', 'backward:seller_registration_number'):
            #     from keyboards.reply.delete_reply_markup import delete_reply_markup
            #     await delete_reply_markup(event)
            #     return False
            if event.data == 'rewrite_seller_number':
                ic()
                # await send_reply_button_contact(event)
                return False

        elif isinstance(event, Message) and event.text == '/start':
            return False
        else:
            ic(event.text)
        ic()
        return True
    def get_user_id(self, request):
        ic(request)
        if request:
            return request.from_user.id
        return None

    # async def is_user_blocked(self, user_id: int) -> bool:
    #     return user_id in global_blocked_users and datetime.now() < global_blocked_users[user_id]
    #
    # async def check_rate_limit(self, user_id: int) -> bool:
    #     current_time = datetime.now()
    #     user_data = global_user_message_counts.get(user_id, {'count': 0, 'time': current_time})
    #     if (current_time - user_data['time']).total_seconds() < self.rate_limit:
    #         user_data['count'] += 1
    #         if user_data['count'] > self.spam_detection_count:
    #             return False  # Превышение лимита сообщений
    #     else:
    #         user_data['count'] = 1
    #         user_data['time'] = current_time
    #     global_user_message_counts[user_id] = user_data
    #     return True
    #
    # async def check_long_term_spam(self, user_id: int) -> bool:
    #     current_time = datetime.now()
    #     long_term_data = global_long_term_user_message_counts.get(user_id, {'count': 0, 'time': current_time})
    #     if (current_time - long_term_data['time']).total_seconds() <= self.long_term_duration:
    #         long_term_data['count'] += 1
    #         if long_term_data['count'] >= self.long_term_spam_count:
    #             return False  # Пользователь считается длительным спамером
    #     else:
    #         long_term_data['count'] = 1
    #         long_term_data['time'] = current_time
    #     global_long_term_user_message_counts[user_id] = long_term_data
    #     return True
    #
    # async def block_user(self, user_id: int, duration: int, mode: str, data, time):
    #     ic()
    #     end_block_time = datetime.now() + timedelta(seconds=duration)
    #     global_blocked_users[user_id] = end_block_time
    #     # Отправка уведомления пользователю о блокировке
    #     await self.notify_user(user_id, duration, mode, data)
    #
    # async def notify_user(self, user_id: int, duration: int, mode: str, data):
    #     bot = data.get('bot')
    #     ic(bot)
    #     message = lexicon_module.LEXICON['spam_detected']
    #     if bot:
    #         try:
    #             await bot.send_message(user_id, message.format(duration=duration, mode=mode))
    #         except Exception as e:
    #             traceback.print_exc()
    #             print(f"Error sending notification: {e}")
    #
