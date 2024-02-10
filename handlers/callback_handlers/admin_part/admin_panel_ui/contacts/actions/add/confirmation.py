from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.choose_type import ChooseContactsTypeHandler
from handlers.custom_filters.correct_number import CheckInputNumber
from states.admin_part_states.tech_support_states import TechSupportStates
from utils.lexicon_utils.admin_lexicon.contacts_lexicon import ADMIN_CONTACTS
from utils.oop_handlers_engineering.update_handlers.base_objects.base_message_handler_init import BaseMessageHandler


class ConfirmationAddNewContactHandler(BaseMessageHandler):
    async def process_message(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.set_state(state, TechSupportStates.review)
        lexicon_part = await self.get_lexicon_part(request, state)
        if lexicon_part:
            self.output_methods = [
                self.menu_manager.travel_editor(
                    lexicon_part=lexicon_part,
                    delete_mode=await self.incorrect_manager.get_incorrect_flag(state)
                )
            ]

    async def get_lexicon_part(self, request, state):
        memory_storage = await state.get_data()
        contact_type = memory_storage.get('contact_type')

        if isinstance(request, Message) and contact_type:
            contact_type_string = ADMIN_CONTACTS[f'link_name:{contact_type}']
            contact_link = request.text

            if contact_type == 'telegram':
                contact_type_string = contact_type_string.split('(')[0].strip()
            else:
                raw_contact_link = contact_link.strip().replace(' ', '')
                contact_link = await CheckInputNumber().format_and_validate_phone_number(raw_contact_link)

            lexicon_part = ADMIN_CONTACTS['confirmation_add_contact']
            lexicon_part['message_text'] = lexicon_part['message_text'].format(
                contact_type=ADMIN_CONTACTS[f'contact_type_{contact_type}'],
                contact_entity=ADMIN_CONTACTS[contact_type], contact=contact_link)

            await state.update_data(contact_link=contact_link)
            return lexicon_part
        else:
            await self.send_alert_answer(request, ADMIN_CONTACTS['contact_type_was_not_found'])
            await ChooseContactsTypeHandler().callback_handler(request, state)
