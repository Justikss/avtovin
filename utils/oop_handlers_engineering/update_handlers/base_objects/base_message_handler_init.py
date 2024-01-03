from abc import ABC
from typing import List

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_admin_pagination import \
    AdminPaginationInit
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_inline_pagination import \
    InlinePaginationInit
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_travel_editor import \
    TravelMessageEditorInit
from utils.oop_handlers_engineering.update_handlers.base_objects.base_handler import BaseHandler


class BaseMessageHandler(BaseHandler, ABC):
    def __init__(self,
                 output_methods: List[AdminPaginationInit | InlinePaginationInit | TravelMessageEditorInit] = None,
                 filters=None):
        self.filters: List[BaseFilter] = self.unpack_filters(filters)
        super().__init__(output_methods)

    def unpack_filters(self, filters):
        if not isinstance(filters, list):
            if filters is None:
                filters = []
            else:
                filters = [filters]

        return filters

    async def message_handler(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        if self.filters is None:
            self.filters = []
        elif not isinstance(self.filters, list):
            self.filters = [self.filters]
        ic(self.filters)

        if all([ic(await filter_object(request, state)) for filter_object in self.filters]):
            ic()
            await self.process_message(request, state, **kwargs)

            if isinstance(request, Message):
                self.message_text = request.text.replace('<', '&lt;').replace('>', '&gt;')

            await self.output_panel(request, state)



    async def process_message(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        pass



