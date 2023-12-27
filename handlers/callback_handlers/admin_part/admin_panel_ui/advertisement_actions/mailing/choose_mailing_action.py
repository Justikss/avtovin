import importlib

from aiogram import types
from aiogram.fsm.context import FSMContext

from utils.lexicon_utils.Lexicon import ADVERT_LEXICON

message_editor_module = importlib.import_module('handlers.message_editor')

async def request_choose_mailing_action(callback: types.CallbackQuery, state: FSMContext):
    if await state.get_state():
        await state.clear()
    lexicon_part = ADVERT_LEXICON['choose_mailing_action']
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part,
                                                           delete_mode=True)