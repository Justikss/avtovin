from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.input_mailing_data.edit_mailing_data.edit_data_controller import \
    edit_mailing_data_controller
from states.admin_part_states.mailing.mailing_setup_states import MailingStates
import importlib

# Импорт модуля редактирования сообщений через importlib
Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
message_editor_module = importlib.import_module('handlers.message_editor')

async def request_mailing_recipients(request: types.Message | types.CallbackQuery, state: FSMContext, mailing_datetime=None):
    if mailing_datetime:
        await state.update_data(mailing_datetime=mailing_datetime)

    if await edit_mailing_data_controller(request, state, None):
        return

    lexicon_part = Lexicon_module.ADVERT_LEXICON['enter_mailing_recipients']
    await state.set_state(MailingStates.enter_recipients)
    await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                           delete_mode=True)
