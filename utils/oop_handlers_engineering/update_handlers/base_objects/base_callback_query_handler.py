from abc import ABC
from typing import List, Optional

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, CallbackQuery


from utils.oop_handlers_engineering.update_handlers.base_objects.base_handler import BaseHandler


class BaseCallbackQueryHandler(BaseHandler, ABC):
    async def callback_handler(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # Обработка callback
        await self.process_callback(request, state, **kwargs)

        # Генерация меню
        await self.output_panel(request, state)
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # Определить в подклассах
        if isinstance(request, CallbackQuery):
            await request.answer()

