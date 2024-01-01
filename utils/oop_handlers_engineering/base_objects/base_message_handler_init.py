from typing import List

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.oop_handlers_engineering.base_objects.generate_output_objects.specific_objects.base_admin_pagination import \
    AdminPaginationInit
from utils.oop_handlers_engineering.base_objects.generate_output_objects.specific_objects.base_inline_pagination import \
    InlinePaginationInit
from utils.oop_handlers_engineering.base_objects.generate_output_objects.specific_objects.base_travel_editor import \
    TravelMessageEditorInit


class BaseMessageHandler:
    def __init__(self,
                 output_methods: List[AdminPaginationInit | InlinePaginationInit | TravelMessageEditorInit] = None,
                 filters=None):
        self.output_methods = output_methods

        self.filters: List[BaseFilter] = filters

    async def handle_message(self, request: Message | CallbackQuery, state: FSMContext, incorrect=False):
        if self.filters is None:
            self.filters = []
        if all([await filter(request) for filter in self.filters]):
            await self.process_message(request, state, incorrect)

    async def process_message(self):
        pass

    async def process_output(self, message: Message, state: FSMContext, incorrect):
        # Определить в подклассах
        if self.output_methods:
            for output_class in self.output_methods:
                await output_class.process()

