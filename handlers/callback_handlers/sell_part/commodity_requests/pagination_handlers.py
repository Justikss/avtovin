import importlib
from abc import ABC

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from handlers.callback_handlers.sell_part.commodity_requests.output_sellers_requests import Pagination, output_sellers_commodity_page
from utils.Lexicon import LexiconSellerRequests as Lexicon

class SellerRequestsPagination(ABC):
    @staticmethod
    async def pagination_button(callback: CallbackQuery, state: FSMContext, pagination_operation=None):
        redis_module = importlib.import_module('handlers.message_editor')  # Ленивый импорт
        user_id = str(callback.from_user.id)
        seller_requests_pagination = await redis_module.redis_data.get_data(
            key=user_id + ':seller_requests_pagination', use_json=True)
        if seller_requests_pagination and seller_requests_pagination != 'null':
            print(seller_requests_pagination)
            seller_requests_pagination = Pagination(**seller_requests_pagination)

            if seller_requests_pagination.current_page == 0:
                seller_requests_pagination.current_page += 1

            output_data_part = await seller_requests_pagination.get_page(pagination_operation)
            if output_data_part:
                await redis_module.redis_data.set_data(key=user_id + ':seller_requests_pagination',
                                                       value=await seller_requests_pagination.to_dict())

                media_group_delete_module = importlib.import_module('handlers.callback_handlers.sell_part.seller_main_menu')

                await media_group_delete_module.delete_media_groups(request=callback)


                return await output_sellers_commodity_page(request=callback, output_data_part=output_data_part, state=state)

        await callback.answer(Lexicon.pages_were_end)


class SellerRequestPaginationHandlers(SellerRequestsPagination):
    @staticmethod
    async def right_button(callback: CallbackQuery, state: FSMContext, pagination_operation=None):
        pagination_operation = '+'
        await SellerRequestPaginationHandlers.pagination_button(callback, state, pagination_operation)

    @staticmethod
    async def left_button(callback: CallbackQuery, state: FSMContext, pagination_operation=None):
        pagination_operation = '-'
        await SellerRequestPaginationHandlers.pagination_button(callback, state, pagination_operation)


