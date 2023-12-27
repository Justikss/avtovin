import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from utils.lexicon_utils.Lexicon import ADVERT_LEXICON


async def choose_advertisement_action(callback: CallbackQuery, state: FSMContext):
    message_editor_module = importlib.import_module('handlers.message_editor')

    if await state.get_state():
        await state.clear()
    lexicon_part = ADVERT_LEXICON['choose_advert_action']

    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='',
                                                           lexicon_part=lexicon_part, delete_mode=True)
