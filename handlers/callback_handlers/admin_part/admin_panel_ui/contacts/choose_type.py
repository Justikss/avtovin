from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.lexicon_utils.admin_lexicon.contacts_lexicon import ADMIN_CONTACTS
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class ChooseContactsTypeHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        if await state.get_state():
            await state.clear()

        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=ADMIN_CONTACTS['choose_type']
            )
        ]