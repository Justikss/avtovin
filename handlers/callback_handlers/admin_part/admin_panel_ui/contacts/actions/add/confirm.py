from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.tech_supports import TechSupportsManager
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.choose_type import ChooseContactsTypeHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.output.list import ContactListHandler
from states.admin_part_states.tech_support_states import TechSupportStates
from utils.lexicon_utils.admin_lexicon.contacts_lexicon import ADMIN_CONTACTS
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class ConfirmAddNewContactHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic()
        memory_storage = await state.get_data()
        contact_type = memory_storage.get('contact_type')
        contact_link = memory_storage.get('contact_link')
        insert_query = await TechSupportsManager.insert(contact_type, contact_link)
        if insert_query:
            await self.send_alert_answer(request, ADMIN_CONTACTS['successfully'])
            await ContactListHandler().callback_handler(request, state)
            return
        else:
            await self.send_alert_answer(request, ADMIN_CONTACTS['contact_type_was_not_found'])
            await ChooseContactsTypeHandler().callback_handler(request, state)