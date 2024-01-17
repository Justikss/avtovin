from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.tech_supports import TechSupportsManager
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.choose_type import ChooseContactsTypeHandler
from handlers.custom_filters.correct_number import CheckInputNumber
from states.admin_part_states.tech_support_states import TechSupportStates
from utils.lexicon_utils.admin_lexicon.contacts_lexicon import ADMIN_CONTACTS

from utils.oop_handlers_engineering.update_handlers.base_objects.base_message_handler_init import BaseMessageHandler


class ConfirmationRewriteExistsTSContact(BaseMessageHandler):
    async def process_message(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):

        await state.set_state(TechSupportStates.review)
        inputted_link = await self.get_new_link(request, state)
        lexicon_part = await self.get_lexicon_part(request, state, inputted_link)
        if lexicon_part:
            self.output_methods = [
                self.menu_manager.travel_editor(
                    lexicon_part=lexicon_part,
                    delete_mode=await self.incorrect_manager.get_incorrect_flag(state)
                )
            ]

    async def get_new_link(self, request, state):
        memory_storage = await state.get_data()
        contact_entity = memory_storage.get('contact_type')
        contact_link = request.text
        if contact_entity == 'number':
            raw_contact_link = contact_link.strip().replace(' ', '')
            contact_link = await CheckInputNumber().format_and_validate_phone_number(raw_contact_link)

        await state.update_data(contact_link=contact_link)
        return contact_link

    async def get_lexicon_part(self, request, state, new_link):
        memory_storage = await state.get_data()
        contact_entity = memory_storage.get('contact_type')
        contact_id = memory_storage.get('contact_id')
        contact_model = await TechSupportsManager.get_specific(contact_id)

        if all((contact_id, contact_model, contact_entity, new_link)):
            lexicon_part = ADMIN_CONTACTS['confirmation_rewrite_exist_contact']
            lexicon_part['message_text'] = lexicon_part['message_text'].format(
                link=ADMIN_CONTACTS[contact_entity],
                cur_link=contact_model.link,
                new_link=new_link)
            return lexicon_part
        else:
            await self.send_alert_answer(request, ADMIN_CONTACTS['contact_type_or_id_was_not_found'])
            await ChooseContactsTypeHandler().callback_handler(request, state)



