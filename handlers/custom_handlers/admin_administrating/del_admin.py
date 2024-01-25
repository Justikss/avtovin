from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.oop_handlers_engineering.update_handlers.base_objects.base_admin_administrate_object import \
    BaseAdminCommandHandler


class DelAdminHandler(BaseAdminCommandHandler):
    async def process_message(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # await super().message_handler(request, state, **kwargs)

        user_id = await self.get_user_id(request)

        if await self.user_id_not_found_handler(request, user_id):
            return
        else:
            query = await self.admin_manager.remove_admin(
                user_id
            )

            if query:
                await self.logging_action(request, subject=request.text, action='del_admin')

            await self.query_state_callback(request, query, action_on='admin')
