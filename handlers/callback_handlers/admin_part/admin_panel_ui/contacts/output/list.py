from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.tech_supports import TechSupportsManager
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.statistic_manager import \
    EmptyField
from states.admin_part_states.tech_support_states import TechSupportStates
from utils.lexicon_utils.admin_lexicon.contacts_lexicon import OutputTSContacts
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler


class ContactListHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.set_state(state, TechSupportStates.review)
        await self.incorrect_manager.try_delete_incorrect_message(request, state)
        self.output_methods = [
            self.menu_manager.inline_pagination(
                models_range=await self.get_models_range(request, state),
                lexicon_class=OutputTSContacts,
                page_size=6
            )
        ]

    async def get_models_range(self, request, state):
        if request.data.startswith('ts_contact_type:'):
            contact_type = request.data.split(':')[-1]
            await state.update_data(contact_type=contact_type)
        else:
            memory_storage = await state.get_data()
            contact_type = memory_storage.get('contact_type')

        models_range = await TechSupportsManager.get_by_type(contact_type)

        if not models_range:
            models_range = [EmptyField]

        return models_range