from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config_data.config import DEFAULT_COMMANDS


async def bot_echo(message: Message):
    '''Ответ на сообщения, не попавшие в обработки.'''
    await message.chat.bot.send_message(chat_id=-4006110220,
        text=str(message.chat.id)
    )
