import importlib
from abc import ABC
from typing import List, Optional, Callable

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message

from handlers.utils.message_answer_without_callback import send_message_answer
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_admin_pagination import \
    AdminPaginationInit
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_inline_pagination import \
    InlinePaginationInit
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_travel_editor import \
    TravelMessageEditorInit
from utils.oop_handlers_engineering.update_handlers.base_objects.utils_objects.incorrect_adapter import IncorrectAdapter


class BaseHandler(ABC):
    def __init__(self, output_methods: Optional[List[AdminPaginationInit | InlinePaginationInit | TravelMessageEditorInit]] = None):
        self.output_methods = output_methods
        self.incorrect_manager = IncorrectAdapter()
        self.redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт


    async def send_alert_answer(self, request: Message| CallbackQuery, text: str, show_alert=False):
        await send_message_answer(request, text, show_alert=show_alert)

    async def set_state(self, state: FSMContext, needed_state: State):
        if await state.get_state() != needed_state:
            await state.set_state(needed_state)

    async def output_panel(self, request: CallbackQuery | Message, state: FSMContext):
        if self.output_methods:
            for output_class in self.output_methods:
                if not isinstance(output_class, Callable):
                    callable_object = output_class.process
                else:
                    callable_object = output_class
                await callable_object(request, state)

    async def insert_into_message_text(self, lexicon_part: dict, kwargs_to_insert: dict) -> dict:
        lexicon_part['message_text'] = lexicon_part['message_text'].format(**kwargs_to_insert)
        return lexicon_part