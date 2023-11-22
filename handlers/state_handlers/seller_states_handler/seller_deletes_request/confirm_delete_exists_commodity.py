import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.commodity_requests import CommodityRequester
from handlers.callback_handlers.sell_part.commodity_requests.commodity_requests_handler import \
    commodity_reqests_by_seller
from handlers.callback_handlers.sell_part.commodity_requests.output_sellers_requests_by_car_brand import \
    output_sellers_requests_by_car_brand_handler
from utils.Lexicon import LEXICON
from handlers.callback_handlers.sell_part.commodity_requests.pagination_handlers import output_sellers_commodity_page


async def confirm_delete_exists_commodity_handler(callback: CallbackQuery, state: FSMContext):
    '''Подтверждение удаления заявки на продажу машины'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    media_group_deleter_module = importlib.import_module('utils.chat_cleaner.media_group_messages')

    await media_group_deleter_module.delete_media_groups(request=callback)

    memory_storage = await state.get_data()
    print('memory_storage[car_id]', memory_storage['car_id'])
    delete_response = CommodityRequester.delete_car_by_id(memory_storage['car_id'])
    print('delete_response', delete_response)
    # if delete_response:

    print('delete_response', delete_response)
    await callback.answer(LEXICON['successfully'], show_alert=True)
    await state.clear()
    # chosen_brand = await message_editor.redis_data.get_data(key=str(callback.from_user.id) + ':sellers_requests_car_brand_cache')
    await commodity_reqests_by_seller(callback=callback)
    # else:
    #     await callback.answer(LEXICON['unexpected_behavior'])
