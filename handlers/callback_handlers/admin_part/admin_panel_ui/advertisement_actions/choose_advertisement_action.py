import importlib

from aiogram.types import CallbackQuery

from utils.lexicon_utils.Lexicon import ADVERT_LEXICON


async def choose_advertisement_action(callback: CallbackQuery):
    message_editor_module = importlib.import_module('handlers.message_editor')

    lexicon_part = ADVERT_LEXICON['choose_advert_action']

    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='',
                                                           lexicon_part=lexicon_part, delete_mode=True)
