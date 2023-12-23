from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message


async def delete_message(request: CallbackQuery | Message, message_id):
    match request:
        case CallbackQuery():
            message = request.message
        case Message():
            message = request

    try:
        await message.chat.delete_message(message_id)
    except TelegramBadRequest:
        pass