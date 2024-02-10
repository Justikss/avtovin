import asyncio
import importlib
import logging
import traceback

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message


async def delete_message(request: CallbackQuery | Message, message_id=None, chat_id=None, from_redis=False, bot=None):

    if from_redis:
        from handlers.custom_filters.message_is_photo import MessageIsPhoto
        await MessageIsPhoto().chat_cleaner(trash_redis_keys=(':last_message', ':last_media_group'),
                                            message=request if isinstance(request, Message) else request.message)

        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

        message_id = await redis_module.redis_data.get_data(
            key=f'{request.from_user.id}:last_message')
    if not message_id:
        return


    match request:
        case CallbackQuery():
            message = request.message
        case Message():
            message = request

    if not chat_id:
        chat_id = message.chat.id
    try:
        if isinstance(message_id, list):
            delete_method = request.bot.delete_messages
            message_id_kwarg = {'message_ids': message_id}
        else:
            delete_method = request.bot.delete_message
            message_id_kwarg = {'message_id': message_id}

        delete_query = await delete_method(chat_id=chat_id, **message_id_kwarg)
        logging.debug('HEADER: Удаление сообщения %s: %s', str(message_id), str(delete_query))
    except TelegramBadRequest:
        pass

