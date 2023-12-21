import importlib

from aiogram.types import CallbackQuery

from utils.lexicon_utils.Lexicon import ADMIN_LEXICON


async def choose_seller_category_by_admin_handler(callback: CallbackQuery):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part=ADMIN_LEXICON['select_seller_category'])