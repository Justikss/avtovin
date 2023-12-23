import asyncio
import importlib

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery


async def send_message_answer(request: Message| CallbackQuery, text, sleep_time):
    match request:
        case Message():
            redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

            last_message = await redis_module.redis_data.get_data(key=f'{request.from_user.id}:last_message')
            try:
                await request.chat.delete_message(last_message)
            except TelegramBadRequest:
                pass

            alert_message = await request.answer(text)
            await asyncio.sleep(sleep_time)

            try:
                await request.chat.delete_message(alert_message.message_id)
            except TelegramBadRequest:
                pass
        case CallbackQuery():
            await request.answer(text)
