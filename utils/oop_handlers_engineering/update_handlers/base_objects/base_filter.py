import importlib
from abc import ABC
from typing import Optional

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.memory_storage_incorrect_controller import \
    incorrect
from handlers.utils.delete_message import delete_message


class BaseFilterObject(BaseFilter, ABC):
    def __init__(self):
        self.redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    async def __call__(self, message: Message, state: FSMContext,
                       incorrect_flag=None, message_input_request_handler=None) -> bool:
        '''До наследования функционала определить:
        message_input_request_handler: Callable ,
        incorrect_flag: bool | str'''

        memory_storage = await state.get_data()

        last_admin_answer = memory_storage.get('last_admin_answer')

        if last_admin_answer:
            await delete_message(message, last_admin_answer)

        if incorrect_flag:
            ic()
            await incorrect(state, message.message_id)
            await message_input_request_handler(message, state, incorrect=incorrect_flag)
            return False
        else:
            await delete_message(message, message.message_id)
            ic()
            return True



