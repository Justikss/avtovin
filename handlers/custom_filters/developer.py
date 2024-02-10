from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config_data.config import DEVELOPER_TELEGRAM_ID


class CheckOnDeveloper(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        ic(message.from_user.id, int(DEVELOPER_TELEGRAM_ID), message.from_user.id == int(DEVELOPER_TELEGRAM_ID))
        if message.from_user.id == int(DEVELOPER_TELEGRAM_ID):
            return True