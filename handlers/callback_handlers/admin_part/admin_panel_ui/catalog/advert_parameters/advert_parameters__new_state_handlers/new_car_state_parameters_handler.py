from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class NewCarStateParameters(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        #в мемори стораж:
        selected_parameters # дата выбранного
        current_new_car_parameter # текущий выборный параметр


        await super().process_callback(request, state, **kwargs)