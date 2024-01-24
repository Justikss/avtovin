from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.oop_handlers_engineering.update_handlers.base_objects.base_admin_administrate_object import \
    BaseAdminCommandHandler


class SetAdminHandler(BaseAdminCommandHandler):
    async def process_message(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # await super().message_handler(request, state, **kwargs)

        query = await self.admin_manager.set_admin(
            await self.get_user_id(request)
        )

        await self.query_state_callback(request, query)
