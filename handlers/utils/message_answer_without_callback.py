import asyncio
import importlib
from copy import copy

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from config_data.config import message_answer_awaited


async def send_message_answer(request: Message| CallbackQuery, text, sleep_time=None):
    match request:
        case Message():
            redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
            media_group_delete_module = importlib.import_module('handlers.callback_handlers.sell_part.seller_main_menu')

            last_message = await redis_module.redis_data.get_data(key=f'{request.from_user.id}:last_message')
            try:
                await request.chat.delete_message(last_message)
            except TelegramBadRequest:
                pass
            await media_group_delete_module.delete_media_groups(request=request)

            alert_message = await request.answer(f'<blockquote><b>{copy(text)}</b></blockquote>')
            await asyncio.sleep(message_answer_awaited)

            try:
                await request.chat.delete_message(alert_message.message_id)
            except TelegramBadRequest:
                pass
        case CallbackQuery():
            await request.answer(text)
