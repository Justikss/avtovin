from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.tech_supports import TechSupportsManager
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.choose_type import ChooseContactsTypeHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.output.list import ContactListHandler
from states.admin_part_states.tech_support_states import TechSupportStates
from utils.lexicon_utils.admin_lexicon.contacts_lexicon import ADMIN_CONTACTS
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class ConfirmationDeleteTSContactHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.set_state(state, TechSupportStates.delete_exists)
        lexicon_part = await self.get_lexicon_part(request, state)
        if lexicon_part:
            self.output_methods = [
                self.menu_manager.travel_editor(
                    lexicon_part=lexicon_part
                )
            ]

    async def get_lexicon_part(self, request, state):
        memory_storage = await state.get_data()
        contact_entity = memory_storage.get('contact_type')
        contact_id = memory_storage.get('contact_id')
        if contact_id:
            contact_model = await TechSupportsManager.get_specific(contact_id)
            if contact_model:
                lexicon_part = ADMIN_CONTACTS['start_delete_contact']

                lexicon_part['message_text'] = lexicon_part['message_text'].format(entity=ADMIN_CONTACTS[contact_entity],
                                                                                   link=contact_model.link)
                return lexicon_part

        if not contact_entity:
            await self.send_alert_answer(request, ADMIN_CONTACTS['contact_type_was_not_found'])
            await ChooseContactsTypeHandler().callback_handler(request, state)
        else:
            await self.send_alert_answer(request, ADMIN_CONTACTS['contact_was_not_found'])
            await ContactListHandler().callback_handler(request, state)
