import importlib
from abc import ABC
from typing import List, Optional, Callable

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message

from handlers.utils.delete_message import delete_message
from handlers.utils.message_answer_without_callback import send_message_answer
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.output_generator_manager import \
    MenuGenerator, AdminPaginationInit, InlinePaginationInit, TravelMessageEditorInit
from utils.oop_handlers_engineering.update_handlers.base_objects.utils_objects.incorrect_adapter import IncorrectAdapter


class BaseHandler(ABC):
    def __init__(self, output_methods: Optional[List[AdminPaginationInit | InlinePaginationInit | TravelMessageEditorInit]] = None):
        self.output_methods = output_methods
        self.incorrect_manager = IncorrectAdapter()
        self.redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        self.menu_manager = MenuGenerator

    async def send_alert_answer(self, request: Message| CallbackQuery, text: str, show_alert=False):
        await send_message_answer(request, text, show_alert=show_alert)

    async def set_state(self, state: FSMContext, needed_state: State):
        ic(await state.get_state())
        if await state.get_state() != needed_state:
            await state.set_state(needed_state)
        else:
            return 'exists'
        ic(await state.get_state())


    async def _output_panel(self, request: CallbackQuery | Message, state: FSMContext):
        if self.output_methods:
            ic(len(self.output_methods))
            for output_class in self.output_methods:
                if output_class:
                    if not isinstance(output_class, Callable):
                        callable_object = output_class.process
                    else:
                        callable_object = output_class

                    await callable_object(request, state)

    async def insert_into_message_text(self, lexicon_part: dict, kwargs_to_insert: dict) -> dict:
        lexicon_part['message_text'] = lexicon_part['message_text'].format(**kwargs_to_insert)
        return lexicon_part

    async def logging_action(self, request, action, subject='', reason=False):
        await log_admin_action(request.from_user.username, action, subject=subject, reason=reason)

    async def clean_state(self, state: FSMContext):
        if await state.get_state():
            await state.clear()

    async def message_object(self, request: CallbackQuery | Message):
        if isinstance(request, CallbackQuery):
            message_object = request.message
        else:
            message_object = request
        return message_object