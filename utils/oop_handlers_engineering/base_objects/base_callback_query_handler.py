from typing import List

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.oop_handlers_engineering.base_objects.generate_output_objects.specific_objects.base_admin_pagination import \
    AdminPaginationInit
from utils.oop_handlers_engineering.base_objects.generate_output_objects.specific_objects.base_inline_pagination import \
    InlinePaginationInit
from utils.oop_handlers_engineering.base_objects.generate_output_objects.specific_objects.base_travel_editor import \
    TravelMessageEditorInit


class BaseCallbackQueryHandler:
    def __init__(self, output_methods: List[AdminPaginationInit | InlinePaginationInit | TravelMessageEditorInit]):
        self.output_methods = output_methods

    async def handle_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # Обработка callback
        await self.process_callback(request)

        # Генерация меню
        if self.output_methods:
            for output_class in self.output_methods:
                await output_class.process()
    async def process_callback(self, callback_query: types.CallbackQuery):
        # Определить в подклассах
        pass