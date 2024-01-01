from typing import List, Optional

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_admin_pagination import \
    AdminPaginationInit
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_inline_pagination import \
    InlinePaginationInit
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_travel_editor import \
    TravelMessageEditorInit


class BaseCallbackQueryHandler:
    def __init__(self, output_methods: Optional[List[AdminPaginationInit | InlinePaginationInit | TravelMessageEditorInit]] = None):
        self.output_methods = output_methods

    async def callback_handler(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # Обработка callback
        await self.process_callback(request, state, **kwargs)

        # Генерация меню
        if self.output_methods:
            for output_class in self.output_methods:
                await output_class.process(request, state)
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # Определить в подклассах
        pass