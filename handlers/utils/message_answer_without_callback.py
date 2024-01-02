import asyncio
import importlib
from copy import copy
from datetime import datetime

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from config_data.config import message_answer_awaited


async def send_message_answer(request: Message | CallbackQuery, text: str, sleep_time=None):
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
            text = f'<blockquote><b>{copy(text)}</b></blockquote>'
            alert_message = await request.answer(text)

            for time_point in range(3, 0, -1):
                await alert_message.edit_text(text=f'{text}{time_point}...')
                await asyncio.sleep(message_answer_awaited / 3)

            try:
                await request.chat.delete_message(alert_message.message_id)
            except TelegramBadRequest:
                pass
        case CallbackQuery():
            await request.answer(text)
