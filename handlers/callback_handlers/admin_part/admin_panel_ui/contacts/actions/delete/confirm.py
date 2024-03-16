from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.tech_supports import TechSupportsManager
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.choose_type import ChooseContactsTypeHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.output.list import ContactListHandler
from utils.lexicon_utils.admin_lexicon.contacts_lexicon import ADMIN_CONTACTS
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class ConfirmDeleteTSContactHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        memory_storage = await state.get_data()
        contact_id = memory_storage.get('contact_id')
        contact_entity = memory_storage.get('contact_type')

        if contact_id:
            await TechSupportsManager.delete(contact_id)
            await self.send_alert_answer(request, ADMIN_CONTACTS['successfully'])
            if contact_entity:
                await ContactListHandler().callback_handler(request, state)
                return
            else:
                await self.send_alert_answer(request, ADMIN_CONTACTS['contact_type_was_not_found'])
                await ChooseContactsTypeHandler().callback_handler(request, state)
                return
        else:
            await self.send_alert_answer(request, ADMIN_CONTACTS['contact_id_was_not_found'])
            await ContactListHandler().callback_handler(request, state)
            return
