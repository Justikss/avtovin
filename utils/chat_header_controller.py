import importlib
import traceback
from typing import Union

from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest

from config_data.config import header_message_text


async def header_controller(request: Union[CallbackQuery, Message], need_delete=False):
    redis_module = importlib.import_module('utils.redis_for_language')
    header_message_id = await redis_module.redis_data.get_data(key=f'{request.from_user.id}:bot_header_message')
    if isinstance(request, Message):
        message = request
    else:
        message = request.message
    send_flag = False
    copied_message = None

    if not header_message_id:
        send_flag = True
    else:
        try:
            if need_delete:
                await message.chat.bot.delete_message(chat_id=message.chat.id, message_id=header_message_id)
                send_flag = True

            await message.chat.bot.edit_message_text(chat_id=message.chat.id, text=f'{header_message_text}.',
                                                message_id=header_message_id)
            await message.chat.bot.edit_message_text(chat_id=message.chat.id, text=f'{header_message_text}..',
                                                     message_id=header_message_id)
            await message.chat.bot.edit_message_text(chat_id=message.chat.id, text=header_message_text,
                                                     message_id=header_message_id)
            # copied_message = await message.chat.bot.copy_message(chat_id='-4084384240', from_chat_id=message.chat.id,
            #                                                      message_id=header_message_id)
        except TelegramBadRequest as ex:
            # ic(ex)
            # traceback.print_exc()
            send_flag = True

    if send_flag and (request.from_user.id == message.chat.id):
        ic(send_flag)
        new_header_message = await message.bot.send_message(chat_id=message.chat.id, text=header_message_text)
        try:
            await redis_module.redis_data.set_data(key=f'{request.from_user.id}:bot_header_message', value=new_header_message.message_id)
        except Exception as ex:
            ic(ex)
            traceback.print_exc()
            ic(new_header_message.message_id)
            pass

        redis_key = str(request.from_user.id) + ':last_message'
        last_message_id = await redis_module.redis_data.get_data(redis_key)
        try:
            await message.chat.bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)
        except:
            pass
        return True