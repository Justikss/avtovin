import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.tech_supports import TechSupportsManager
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.actions.add.start import StartAddNewContactHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.actions.rewrite.start import \
    StartRewriteExistsTSContact
from handlers.custom_filters.correct_number import CheckInputNumber
from utils.oop_handlers_engineering.update_handlers.base_objects.base_filter import BaseFilterObject


class InputTSLinkFilter(BaseFilterObject):
    async def __call__(self, request: Message | CallbackQuery, state: FSMContext,
                       incorrect_flag=None,
                       message_input_request_handler=None):
        config_module = importlib.import_module('config_data.config')
        match str(await state.get_state()):
            case 'TechSupportStates:add_new':
                message_input_request_handler = StartAddNewContactHandler().callback_handler
            case 'TechSupportStates:rewrite_exists':
                message_input_request_handler = StartRewriteExistsTSContact().callback_handler

        message_text = request.text
        if len(message_text) > config_module.max_contact_info_len:
            incorrect_flag = 'symbols'
        else:
            memory_storage = await state.get_data()
            contacts_type = memory_storage.get('contact_type')
            match contacts_type:
                case 'telegram':
                    link = message_text
                    if '@' not in link:
                        incorrect_flag = '@'
                case 'number':
                    phonenumber = message_text.strip().replace(' ', '')
                    link = await CheckInputNumber().format_and_validate_phone_number(phonenumber)
                    if not link:
                        incorrect_flag = 'number'

            exists_contact = await TechSupportsManager.get_by_link(link)
            if exists_contact:
                incorrect_flag = 'exists'
            ic(incorrect_flag)
        return await super().__call__(request, state, incorrect_flag, message_input_request_handler)
