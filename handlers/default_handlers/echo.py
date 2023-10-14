from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config_data.config import DEFAULT_COMMANDS


async def bot_echo(message: Message):
    '''Ответ на сообщения, не попавшие в обработки.'''
    await message.reply(
        text=message.text
    )
