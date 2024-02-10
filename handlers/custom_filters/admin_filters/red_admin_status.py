from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.data_requests.admin_requests import AdminManager
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON
from utils.oop_handlers_engineering.update_handlers.base_objects.base_filter import BaseFilterObject

class RedAdminStatus(BaseFilterObject):
    async def __call__(self, request: Message | CallbackQuery, state: FSMContext,
                       incorrect_flag=None, message_input_request_handler=None) -> bool:
        is_red_admin = await AdminManager.admin_authentication(request.from_user.id, 1)
        ic(is_red_admin)
        await self.delete_message(request, request.message_id)

        if is_red_admin:
            return True
        else:
            await self.delete_message(request, request.message_id)
            await self.alert_answer(request, ADMIN_LEXICON['admin_not_is_red'])