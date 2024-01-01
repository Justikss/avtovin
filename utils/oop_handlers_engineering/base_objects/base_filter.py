from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class BaseFilterObject(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        # Базовая реализация, которую нужно переопределить в подклассах
        pass