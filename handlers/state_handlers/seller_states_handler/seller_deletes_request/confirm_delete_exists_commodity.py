from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.commodity_requests import CommodityRequester
from utils.Lexicon import LEXICON
from handlers.callback_handlers.sell_part.commodity_requests.pagination_handlers import output_sellers_commodity_page


async def confirm_delete_exists_commodity_handler(callback: CallbackQuery, state: FSMContext):
    '''Подтверждение удаления заявки на продажу машины'''
    memory_storage = await state.get_data()
    delete_response = CommodityRequester.delete_car_by_id(memory_storage['car_id'])
    if delete_response:
        await callback.answer(LEXICON['successfully'])
        await state.clear()
        await output_sellers_commodity_page(callback=callback)
    else:
        await callback.answer(LEXICON['unexpected_behavior'])
