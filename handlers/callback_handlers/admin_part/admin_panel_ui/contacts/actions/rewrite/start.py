from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.tech_supports import TechSupportsManager
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.choose_type import ChooseContactsTypeHandler
from states.admin_part_states.tech_support_states import TechSupportStates
from utils.lexicon_utils.admin_lexicon.contacts_lexicon import ADMIN_CONTACTS
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class StartRewriteExistsTSContact(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.set_state(state, TechSupportStates.rewrite_exists)
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
        contact_entity = memory_storage.get('contact_type')
        contact_id = memory_storage.get('contact_id')

        if contact_id:
            contact_model = await TechSupportsManager.get_specific(contact_id)

            if contact_model:
                await state.update_data(contact_link=contact_model.link)

                lexicon_key = 'start_rewrite_exists_contact'
                lexicon_part = ADMIN_CONTACTS[lexicon_key]
                if incorrect:
                    incorrect_key = 'add_new_contact'
                    lexicon_part['message_text'] += ADMIN_CONTACTS[f'{incorrect_key}:{incorrect}']
                lexicon_part['message_text'] = lexicon_part['message_text'].format(
                    contact_type=ADMIN_CONTACTS[f'contact_type_{contact_entity}'],
                    entity=ADMIN_CONTACTS[contact_entity],
                    cur_link=contact_model.link,
                    link=ADMIN_CONTACTS[f'link_name:{contact_entity}'])
                return lexicon_part


            else:
                await self.send_alert_answer(request, ADMIN_CONTACTS['contact_type_was_not_found'])
                await ChooseContactsTypeHandler().callback_handler(request, state)
                return
        else:
            await self.send_alert_answer(request, ADMIN_CONTACTS['contact_id_was_not_found'])
            await ChooseContactsTypeHandler().callback_handler(request, state)
            return
