from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler import output_choose
from utils.oop_handlers_engineering.base_objects.generate_output_objects.specific_objects.base_admin_pagination import OutputObject

class InlinePaginationInit(OutputObject):
    def __init__(self, request: Message | CallbackQuery, state: FSMContext,
                 lexicon_class: object, models_range: list, page_size: int):
        self.request = request
        self.state = state
        self.lexicon_class = lexicon_class
        self.model_range = models_range
        self.page_size = page_size
        self.method = output_choose

    async def process(self):
        await self.method(self.request, self.state, self.lexicon_class, self.model_range, self.page_size)
