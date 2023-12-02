from aiogram.types import CallbackQuery
import importlib

from utils.Lexicon import LEXICON

async def seller_faq(callback: CallbackQuery):
    message_editor_module = importlib.import_module('handlers.message_editor')
    
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='seller_faq')
    await callback.answer()
