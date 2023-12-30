import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.input_mailing_data.input_date import \
    request_mailing_date_time
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.input_mailing_data.input_media import \
    request_mailing_media
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.input_mailing_data.input_text import \
    enter_mailing_text


async def edit_field_handler(callback: CallbackQuery, state: FSMContext):
    match callback.data:
        case 'edit_mailing_text':
            await enter_mailing_text(callback, state)
        case 'edit_mailing_media':
            await request_mailing_media(callback, state)
        case 'edit_mailing_date':
            await request_mailing_date_time(callback, state)
        case 'edit_mailing_recipients':
            input_recipients_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.input_mailing_data.input_recipients')
            await input_recipients_module.request_mailing_recipients(callback, state)