from aiogram.types import CallbackQuery
import importlib

async def commodity_reqests_by_seller(callback: CallbackQuery, delete_mode=False):
    message_editor_module = importlib.import_module('handlers.message_editor')

    lexicon_code = 'seller_requests'
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key=lexicon_code, delete_mode=delete_mode)
    await callback.answer()

