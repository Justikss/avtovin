import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils.oop_handlers_engineering.generate_output_objects.base_objects.base_output_object import OutputObject

admin_pagination_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_pagination')

class AdminPaginationInit(OutputObject):
    def __init__(self, pagination_data: list):
        self.pagination_data = pagination_data
        self.class_object = admin_pagination_module.AdminPaginationOutput

    async def process(self, request: Message | CallbackQuery, state: FSMContext = None):
        await self.class_object.set_pagination_data(request, state, self.pagination_data)
