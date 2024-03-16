import asyncio
import importlib
import logging
import traceback
from typing import Union

from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.exceptions import TelegramBadRequest

from config_data.config import anti_spam_duration
from handlers.utils.delete_message import delete_message

config_module = importlib.import_module('config_data.config')

async def header_controller(request: Union[CallbackQuery, Message], need_delete=False, reply_markup=None):
    redis_module = importlib.import_module('utils.redis_for_language')
    header_message_id = await redis_module.redis_data.get_data(key=f'{request.from_user.id}:bot_header_message')
    if isinstance(request, Message):
        message = request
    else:
        message = request.message
    send_flag = False
    copied_message = None
    header_message_text = config_module.header_message_text['text']
    ic()
    ic(header_message_id)
    ic(need_delete)
    if need_delete and header_message_id:
        ic()
        await delete_message(message, header_message_id)
        send_flag = True
        # return
    elif not header_message_id:
        ic()
        send_flag = True
    else:
        ic()
        try:
            ic(message.chat.id)
            # await message.chat.bot.edit_message_text(chat_id=message.chat.id, text=f'{header_message_text}.',
            #                                     message_id=header_message_id)
            await message.chat.bot.edit_message_text(chat_id=message.chat.id, text=f'{header_message_text}..',
                                                     message_id=header_message_id)
            await message.chat.bot.edit_message_text(chat_id=message.chat.id, text=header_message_text,
                                                     message_id=header_message_id)
            ic()
            # copied_message = await message.chat.bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,
            #                                                      message_id=header_message_id)
        except TelegramBadRequest as ex:
            await delete_message(request, header_message_id)
            ic(ex)
            # traceback.print_exc()
            send_flag = True
    ic((request.from_user.id == message.chat.id))
    if send_flag: #and (request.from_user.id == message.chat.id):
        ic(send_flag)
        new_header_message = await message.bot.send_message(chat_id=message.chat.id, text=header_message_text,
                                                            reply_markup=reply_markup)
        ic(reply_markup)
        logging.debug('HEADER: Отправка сообщения: %s', str(new_header_message.message_id))
        # if isinstance(reply_markup, ReplyKeyboardRemove):
        #     logging.debug('HEADER Отправка сообщения: %s c REPLYREMOVE', str(new_header_message.message_id))
        #     await message.chat.bot.edit_message_reply_markup(chat_id=message.chat.id, reply_markup=None,
        #                                              message_id=new_header_message.message_id)
        try:
            await redis_module.redis_data.set_data(key=f'{request.from_user.id}:bot_header_message', value=new_header_message.message_id)
        except Exception as ex:
            ic(ex)
            # traceback.print_exc()
            ic(new_header_message.message_id)
            pass

        redis_key = str(request.from_user.id) + ':last_message'
        last_message_id = await redis_module.redis_data.get_data(redis_key)

        await delete_message(message, last_message_id)

        await asyncio.sleep(anti_spam_duration)
        return True

    else:
        pass
        # ic((request.from_user.id, message.chat.id))
