import importlib

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.review_inputted_data import \
    request_review_mailing_data
from states.admin_part_states.mailing.mailing_setup_states import MailingStates

message_editor_module = importlib.import_module('handlers.message_editor')


Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def start_edit_state(callback, state):
    edit_buttons = Lexicon_module\
        .ADVERT_LEXICON['edit_inputted_data']
    last_message_id = await message_editor_module.redis_data.get_data(key=f'{callback.from_user.id}:last_message')
    edit_keyboard = await message_editor_module.InlineCreator.create_markup(edit_buttons)
    try:
        await callback.message.edit_reply_markup(inline_message_id=last_message_id, reply_markup=edit_keyboard)
    except TelegramBadRequest:
        await request_review_mailing_data(callback, state)


async def edit_mailing_data_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer(Lexicon_module\
                          .ADVERT_LEXICON['edit_mailing_data_alert'], show_alert=True)

    await state.set_state(MailingStates.edit_inputted_data)

    await start_edit_state(callback, state)
    await state.update_data(can_edit_mailing_flag=True)


