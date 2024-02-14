import asyncio
import importlib

from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove


async def delete_reply_markup(request: Message | CallbackQuery):
    # redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

    # last_message_id = await redis_module.redis_data.get_data(key=f'{request.from_user.id}:last_message')

    match request:
        case CallbackQuery():
            chat_id = request.message.chat.id
        case Message():
            chat_id = request.chat.id
        case _:
            return

    # await request.bot.edit_message_reply_markup(chat_id=chat_id, message_id=last_message_id,
    #                                             reply_markup=ReplyKeyboardRemove())
    from handlers.utils.delete_message import delete_message
    config_module = importlib.import_module('config_data.config')

    # await asyncio.sleep(config_module.anti_spam_duration)

    from utils.chat_header_controller import header_controller
    await header_controller(request, True, ReplyKeyboardRemove())

    await asyncio.sleep(config_module.anti_spam_duration)

