import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.get_username import get_username
from utils.oop_handlers_engineering.update_handlers.base_objects.base_admin_administrate_object import \
    BaseAdminCommandHandler


class AdminHelpHandler(BaseAdminCommandHandler):
    async def process_message(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.delete_message(request, request.message_id)
        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=self.admin_lexicon['admin_help'],
                delete_mode=True
            )
        ]
