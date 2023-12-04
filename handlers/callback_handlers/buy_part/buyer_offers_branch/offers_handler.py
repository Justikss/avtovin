import importlib

from aiogram.types import CallbackQuery


async def buyer_offers_callback_handler(callback: CallbackQuery):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='buyer_requests')