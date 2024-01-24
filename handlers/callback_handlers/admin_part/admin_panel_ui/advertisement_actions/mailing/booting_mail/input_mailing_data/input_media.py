from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.input_mailing_data.edit_mailing_data.edit_data_controller import \
    edit_mailing_data_controller
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.incorrect_controller import \
    incorrect_controller
from states.admin_part_states.mailing.mailing_setup_states import MailingStates
import importlib

from utils.lexicon_utils.Lexicon import ADVERT_LEXICON

# Импорт модуля редактирования сообщений через importlib
message_editor_module = importlib.import_module('handlers.message_editor')

async def insert_state_data(request, state, modified_text):
    mailing_text = 1
    if modified_text:
        mailing_text = modified_text
    elif isinstance(request, types.CallbackQuery) and request.data == 'empty_mailing_text':
        mailing_text = ''

    if mailing_text != 1:
        await state.update_data(mailing_text=modified_text)


async def request_mailing_media(request: types.Message | types.CallbackQuery,
                                state: FSMContext, modified_text=None, incorrect=False):
    from utils.oop_handlers_engineering.update_handlers.base_objects.utils_objects.incorrect_adapter import \
        IncorrectAdapter

    await insert_state_data(request, state, modified_text)

    await IncorrectAdapter().try_delete_incorrect_message(request, state)

    if await edit_mailing_data_controller(request, state, incorrect):
        return
    await state.update_data(admin_incorrect_flag=False)

    if isinstance(request, types.CallbackQuery) and request.data == 'add_other_media':
        await state.update_data(add_other_media=True)

    await state.set_state(MailingStates.entering_date_time)
    ic(await state.get_state())
    lexicon_part, reply_to_message = await incorrect_controller(request, state, incorrect,
                                                                'enter_mailing_media',
                                                                current_lexicon=ADVERT_LEXICON)
    await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                           reply_message=reply_to_message, delete_mode=True)
