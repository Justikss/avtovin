from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.choose_type import ChooseContactsTypeHandler
from states.admin_part_states.tech_support_states import TechSupportStates
from utils.lexicon_utils.admin_lexicon.contacts_lexicon import ADMIN_CONTACTS
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class StartAddNewContactHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.set_state(state, TechSupportStates.add_new)
        ic()
        ic()
        lexicon_part = await self.get_lexicon_part(request, state, kwargs.get('incorrect'))
        if lexicon_part:
            self.output_methods = [
                self.menu_manager.travel_editor(
                    lexicon_part=lexicon_part,
                    reply_message=await self.incorrect_manager.get_last_incorrect_message_id(state),
                    delete_mode=await self.incorrect_manager.get_incorrect_flag(state)
                )
            ]
    async def get_lexicon_part(self, request, state, incorrect):
        memory_storage = await state.get_data()
        contacts_type = memory_storage.get('contact_type')
        if contacts_type:

            lexicon_part = ADMIN_CONTACTS['add_new_contact']
            if incorrect:

                lexicon_part['message_text'] += ADMIN_CONTACTS['add_new_contact' + f':{incorrect}']

            lexicon_part['message_text'] = lexicon_part['message_text'].format(
                link=ADMIN_CONTACTS[f'link_name:{contacts_type}']
            )
            return lexicon_part
        else:
            await self.send_alert_answer(request, ADMIN_CONTACTS['contact_type_was_not_found'])
            await ChooseContactsTypeHandler().callback_handler(request, state)
