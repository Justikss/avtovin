
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.tech_supports import TechSupportsManager
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.output.list import ContactListHandler
from states.admin_part_states.tech_support_states import TechSupportStates
from utils.lexicon_utils.admin_lexicon.contacts_lexicon import ADMIN_CONTACTS
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class OutputSpecificContactHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.set_state(state, TechSupportStates.review)
        await self.incorrect_manager.try_delete_incorrect_message(request, state)
        lexicon_part = await self.construct_lexicon_part(request, state)
        if lexicon_part:
            self.output_methods = [
                self.menu_manager.travel_editor(
                    lexicon_part=lexicon_part,
                    dynamic_buttons=2,
                    delete_mode=True
                )
            ]


    async def construct_lexicon_part(self, request, state):
        lexicon_part = ADMIN_CONTACTS['output_contact']

        if request.data.startswith('review_ts_contact:'):
            contact_id = int(request.data.split(':')[-1])
            await state.update_data(contact_id=contact_id)
        else:
            memory_storage = await state.get_data()
            contact_id = memory_storage.get('contact_id')

        if contact_id:
            contact_model = await TechSupportsManager.get_specific(contact_id)
            if contact_model:
                lexicon_part['message_text'] = lexicon_part['message_text'].format(
                    contact_type=ADMIN_CONTACTS[f'contact_type_{contact_model.type}'],
                    contact_entity=ADMIN_CONTACTS[contact_model.type], contact=contact_model.link)
                return lexicon_part

        await self.send_alert_answer(request, ADMIN_CONTACTS['contact_was_not_found'])
        await ContactListHandler().callback_handler(request, state)
        return