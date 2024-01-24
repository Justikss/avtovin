import traceback

from aiogram import Bot
from aiogram.types import Chat

async def get_username(bot: Bot, user_id: int):
    ic(user_id)
    try:
        chat: Chat = await bot.get_chat(chat_id=user_id)
        return chat.username
    except Exception as e:
        # traceback.print_exc()
        return None
