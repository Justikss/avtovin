import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_cars_pagination_system.pagination_system_for_buyer import \
    BuyerCarsPagination


class BuyerPaginationVector:
    @staticmethod
    async def buyer_pagination(callback: CallbackQuery, state: FSMContext):
        redis_module = importlib.import_module('utils.redis_for_language')
        pagination_vector = callback.data.split(':')[-1]

        dicted_data = await redis_module.redis_data.get_data(key=f'{str(callback.from_user.id)}:buyer_cars_pagination',
                                                             use_json=True)

        pagination = BuyerCarsPagination(data=dicted_data.get('data'), page_size=dicted_data.get('page_size'),
                                         current_page=dicted_data.get('current_page'))
        await pagination.send_page(request=callback, operation=pagination_vector, state=state)