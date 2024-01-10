import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_admin_pagination import OutputObject

output_choose_module = importlib.import_module(
    'handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler')


class InlinePaginationInit(OutputObject):
    def __init__(self,
                 lexicon_class: object | str, page_size: int, models_range: list=None, remove_last_pagination_data=True):

        self.lexicon_class = lexicon_class
        self.model_range = models_range
        self.page_size = page_size
        self.remove_last_pagination_data = remove_last_pagination_data
        self.method = output_choose_module.output_choose

    async def process(self, request: Message | CallbackQuery, state: FSMContext = None):
        await self.method(request, state, self.lexicon_class, self.model_range, self.page_size,
                          remove_last_pagination_data=self.remove_last_pagination_data)
