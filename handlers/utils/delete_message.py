import importlib
import traceback

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message


async def delete_message(request: CallbackQuery | Message, message_id=None, chat_id=None, from_redis=False):
    if from_redis:
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

        message_id = await redis_module.redis_data.get_data(
            key=f'{request.from_user.id}:last_message')
    if not message_id:
        return
    if isinstance(message_id, list):
        for message_id_element in message_id:
            ic()
            await delete_message(request, message_id_element, chat_id)
        return

    match request:
        case CallbackQuery():
            message = request.message
        case Message():
            message = request

    if not chat_id:
        chat_id = message.chat.id
    try:
        delete_query = await request.bot.delete_message(chat_id=chat_id, message_id=message_id)
        ic(delete_query)
    except TelegramBadRequest:
        pass

