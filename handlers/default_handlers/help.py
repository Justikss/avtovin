from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config_data.config import DEFAULT_COMMANDS


async def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    await message.reply(text="\n".join(text))
