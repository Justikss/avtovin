from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_pagination import AdminPaginationOutput
from utils.oop_handlers_engineering.base_objects.generate_output_objects.base_objects.base_output_object import OutputObject


class AdminPaginationInit(OutputObject):
    def __init__(self, request: Message | CallbackQuery, state: FSMContext, pagination_data: list):
        self.request = request
        self.state = state
        self.pagination_data = pagination_data
        self.class_object = AdminPaginationOutput

    async def process(self):
        await self.class_object.set_pagination_data(self.request, self.state, self.pagination_data)
