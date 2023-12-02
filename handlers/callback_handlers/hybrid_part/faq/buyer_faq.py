import importlib

from aiogram.types import CallbackQuery


async def buyer_faq(callback: CallbackQuery):
    message_editor_module = importlib.import_module('handlers.message_editor')

    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='buyer_faq')
    await callback.answer()


