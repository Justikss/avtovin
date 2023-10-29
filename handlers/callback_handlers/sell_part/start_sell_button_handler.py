from aiogram.types import CallbackQuery
import importlib


async def start_sell_callback_handler(callback: CallbackQuery):
    message_editor_module = importlib.import_module('handlers.message_editor')

    lexicon_code = 'who_is_seller'
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key=lexicon_code)
