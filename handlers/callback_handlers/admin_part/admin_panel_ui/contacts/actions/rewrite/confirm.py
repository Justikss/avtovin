from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.tech_supports import TechSupportsManager
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.choose_type import ChooseContactsTypeHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.output.list import ContactListHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.output.specific import OutputSpecificContactHandler
from handlers.custom_filters.correct_number import CheckInputNumber
from states.admin_part_states.tech_support_states import TechSupportStates
from utils.lexicon_utils.admin_lexicon.contacts_lexicon import ADMIN_CONTACTS
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

from utils.oop_handlers_engineering.update_handlers.base_objects.base_message_handler_init import BaseMessageHandler


class ConfirmRewriteExistsTSContact(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        return await self.confirm_process(request, state)


    async def confirm_process(self, request, state):
        memory_storage = await state.get_data()
        contact_entity = memory_storage.get('contact_type')
        contact_id = memory_storage.get('contact_id')
        contact_link = memory_storage.get('contact_link')

        if all((contact_id, contact_link)):
            await TechSupportsManager.update(contact_id, contact_link)

            await self.send_alert_answer(request, ADMIN_CONTACTS['successfully'])


            if contact_entity:
                return await OutputSpecificContactHandler().callback_handler(request, state)
            else:
                await self.send_alert_answer(request, ADMIN_CONTACTS['contact_type_was_not_found'])
                await ChooseContactsTypeHandler().callback_handler(request, state)
                return
        else:
            await self.send_alert_answer(request, ADMIN_CONTACTS['contact_id_was_not_found'])
            await ContactListHandler().callback_handler(request, state)
            return

