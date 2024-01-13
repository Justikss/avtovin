from abc import ABC
from typing import Optional, List

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_admin_pagination import \
    AdminPaginationInit
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_inline_pagination import \
    InlinePaginationInit
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_travel_editor import \
    TravelMessageEditorInit
from utils.oop_handlers_engineering.update_handlers.base_objects.base_handler import BaseHandler
from utils.oop_handlers_engineering.update_handlers.base_objects.utils_objects.callback_answer_manager import \
    CallbackAnswerManager


class BaseCallbackQueryHandler(BaseHandler, ABC):
    def __init__(self, output_methods: Optional[List[AdminPaginationInit | InlinePaginationInit | TravelMessageEditorInit]] = None):
        super().__init__(output_methods)
        self.idle_callback_answer = CallbackAnswerManager

    async def callback_handler(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # Обработка callback
        await self.process_callback(request, state, **kwargs)

        ic()
        ic(self.output_methods)
        # Генерация меню
        await self._output_panel(request, state)

    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # Определить в подклассах
        if isinstance(request, CallbackQuery):
            await request.answer()


