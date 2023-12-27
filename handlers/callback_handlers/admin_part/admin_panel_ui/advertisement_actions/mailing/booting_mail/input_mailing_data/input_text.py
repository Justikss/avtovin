import importlib

from aiogram import types
from aiogram.fsm.context import FSMContext

from states.admin_part_states.mailing.mailing_setup_states import MailingStates
from utils.lexicon_utils.Lexicon import ADVERT_LEXICON

# Импорт модуля редактирования сообщений через importlib
message_editor_module = importlib.import_module('handlers.message_editor')

async def enter_mailing_text(request: types.Message | types.CallbackQuery, state: FSMContext):
    await state.set_state(MailingStates.entering_text)
    ic(await state.get_state())
    lexicon_part = ADVERT_LEXICON['enter_mailing_text']
    await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                           delete_mode=True)
    await state.set_state(MailingStates.uploading_media)

