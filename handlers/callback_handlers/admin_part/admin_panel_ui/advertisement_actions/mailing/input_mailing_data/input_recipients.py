
import importlib

from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.utils.delete_message import delete_message
from states.admin_part_states.mailing_setup_states import MailingStates
from utils.lexicon_utils.Lexicon import ADVERT_LEXICON
import importlib

# Импорт модуля редактирования сообщений через importlib
message_editor_module = importlib.import_module('handlers.message_editor')

async def request_mailing_recipients(message: types.Message, state: FSMContext, mailing_datetime=None):
    if mailing_datetime:
        await state.update_data(mailing_datetime=mailing_datetime)

    lexicon_part = ADVERT_LEXICON['enter_mailing_recipients']
    await state.set_state(MailingStates.confirmation)

    await message_editor_module.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=lexicon_part)
