import asyncio
import importlib

from aiogram.types import CallbackQuery, Message


async def send_reply_button_contact(request: Message | CallbackQuery):
    from keyboards.reply.reply_markup_creator import create_reply_markup
    from handlers.utils.delete_message import delete_message
    config_module = importlib.import_module('config_data.config')
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    # match request:
    #     case CallbackQuery():
    #         chat_id = request.message.chat.id
    #     case Message():
    #         chat_id = request.chat.id
    #     case _:
    #         return

    keyboard = await create_reply_markup({lexicon_module.captions['send_phone_number']: True})

    # await asyncio.sleep(config_module.anti_spam_duration)
    from utils.chat_header_controller import header_controller
    await header_controller(request, True, ic(keyboard))
    # delete_reply_markup_message = await request.bot.send_message(reply_markup=keyboard, text='||О||', chat_id=chat_id,
    #                                                              parse_mode="MarkdownV2")

    # await delete_message(request, delete_reply_markup_message.message_id)
    # await asyncio.sleep(config_module.anti_spam_duration)