import importlib

from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.incorrect_controller import \
    incorrect_controller
from handlers.utils.delete_message import delete_message
from states.admin_part_states.mailing_setup_states import MailingStates
from utils.lexicon_utils.Lexicon import ADVERT_LEXICON
import importlib

# Импорт модуля редактирования сообщений через importlib
message_editor_module = importlib.import_module('handlers.message_editor')

async def request_mailing_media(message: types.Message, state: FSMContext, modified_text=None, incorrect=False):

    if modified_text:
        await state.update_data(mailing_text=modified_text)

    await state.set_state(MailingStates.entering_date_time)
    lexicon_part, reply_to_message = await incorrect_controller(message, state, incorrect, 'enter_mailing_media')

    await message_editor_module.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=lexicon_part,
                                                           reply_message=reply_to_message)
