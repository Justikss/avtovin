import traceback

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message


async def delete_message(request: CallbackQuery | Message, message_id, chat_id=None):
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

