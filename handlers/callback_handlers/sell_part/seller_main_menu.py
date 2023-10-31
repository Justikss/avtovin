from aiogram.types import CallbackQuery
import importlib

from utils.Lexicon import LEXICON


async def seller_main_menu(callback: CallbackQuery, bot=None):
    message_editor_module = importlib.import_module('handlers.message_editor')

    lexicon_code = 'seller_main_menu'
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key=lexicon_code, bot=bot)