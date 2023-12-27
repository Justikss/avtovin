import importlib

from aiogram import types
from aiogram.fsm.context import FSMContext

from utils.lexicon_utils.Lexicon import ADVERT_LEXICON

message_editor_module = importlib.import_module('handlers.message_editor')

async def request_choose_mailing_type(callback: types.CallbackQuery, state: FSMContext):
    lexicon_part = ADVERT_LEXICON['choose_type_of_mailing_storage']
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part,
                                                           delete_mode=True, dynamic_buttons=2)