import asyncio

from aiogram.exceptions import TelegramBadRequest


async def send_message_answer(message, text, sleep_time):
    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    await message.answer(text)
    await asyncio.sleep(sleep_time)

    try:
        await message.delete()
    except TelegramBadRequest:
        pass
