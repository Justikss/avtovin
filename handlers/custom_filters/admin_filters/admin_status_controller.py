from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_does_not_exists_handler import admin_exists_checker


class AdminStatusController(BaseFilter):
    async def __call__(self, request: Message | CallbackQuery, state: FSMContext):
        return await admin_exists_checker(request=request)
