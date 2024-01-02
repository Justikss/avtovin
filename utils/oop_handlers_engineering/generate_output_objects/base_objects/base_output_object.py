from abc import ABC

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


class OutputObject(ABC):
    async def process(self, request: Message | CallbackQuery, state: FSMContext = None):
        pass