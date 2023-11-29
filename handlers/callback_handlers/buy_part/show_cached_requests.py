import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from icecream import ic


from handlers.callback_handlers.buy_part.main_menu import main_menu
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_cars_pagination_system.pagination_system_for_buyer import \
    BuyerCarsPagination
from handlers.utils.inline_buttons_pagination_heart import CachedRequestsView
from states.buyer_check_nonconfirm_requests_states import CheckNonConfirmRequestsStates

from utils.Lexicon import LEXICON, LexiconCommodityLoader


async def get_cached_requests__chose_brand(callback: CallbackQuery, state: FSMContext):
    # redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    cached_requests_module = importlib.import_module('database.data_requests.offers_requests')

    cached_brands = await cached_requests_module.CachedOrderRequests.get_cached_brands(buyer_id=callback.from_user.id)
    if not cached_brands:
        if callback.data == 'return_to_choose_requests_brand':
            await main_menu(callback)
        else:
            await callback.answer(text=LEXICON["buyer_haven't_cached_requests"])
            return
    else:
        ic(type(cached_brands))
        # await callback.message.edit_text(text=)
        await CachedRequestsView.choose_brand_for_output(callback, car_brands=cached_brands)
        await state.set_state(CheckNonConfirmRequestsStates.await_input_brand)


async def output_cached_requests(callback: CallbackQuery, state: FSMContext):
    cached_requests_module = importlib.import_module('database.data_requests.offers_requests')
    choose_hybrid_handlers_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.hybrid_handlers')

    car_brand = LexiconCommodityLoader.load_commodity_brand['buttons'][callback.data]
    cars = await cached_requests_module.CachedOrderRequests.get_cache(buyer_id=str(callback.from_user.id), brand=car_brand)
    if cars:
        await state.set_state(CheckNonConfirmRequestsStates.brand_flipping_process)
        formatted_cars_data = await choose_hybrid_handlers_module.get_cars_data_pack(callback=callback, state=state, car_models=cars)
        pagination = BuyerCarsPagination(data=formatted_cars_data, page_size=1, current_page=0)

        await pagination.send_page(request=callback, state=state)
        await state.set_state(CheckNonConfirmRequestsStates.brand_flipping_process)


