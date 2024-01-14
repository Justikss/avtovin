import importlib

from aiogram import types
from aiogram.fsm.context import FSMContext


message_editor_module = importlib.import_module('handlers.message_editor')
Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


async def request_choose_mailing_action(callback: types.CallbackQuery, state: FSMContext):
    if await state.get_state():
        await state.clear()
    lexicon_part = Lexicon_module.ADVERT_LEXICON['choose_mailing_action']
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part,
                                                           delete_mode=True)