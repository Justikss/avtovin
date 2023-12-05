import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from icecream import ic

from handlers.callback_handlers.buy_part.buyer_offers_branch.offers_handler import buyer_offers_callback_handler
# from handlers.callback_handlers.buy_part.main_menu import main_menu
# from handlers.callback_handlers.hybrid_part.return_main_menu import return_main_menu_callback_handler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_cars_pagination_system.pagination_system_for_buyer import \
    BuyerCarsPagination
from handlers.utils.inline_buttons_pagination_heart import CachedRequestsView
from states.buyer_offers_states import CheckNonConfirmRequestsStates, CheckActiveOffersStates

from utils.Lexicon import LEXICON, LexiconCommodityLoader


async def buyer_get_requests__chose_brand(callback: CallbackQuery, state: FSMContext):
    # redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    offer_requester_module = importlib.import_module('database.data_requests.offers_requests')
    buyer_id = str(callback.from_user.id)
    # offer_mode = await redis_module.redis_data.get_data(key=f'{buyer_id}:buyer_offers_mode')
    current_brands = None
    current_state = str(await state.get_state())
    ic(callback.data, current_state)
    if callback.data == 'buyer_cached_offers' or current_state.startswith('CheckNonConfirmRequestsStates'):
        current_brands = await offer_requester_module.CachedOrderRequests.get_offer_brands(buyer_id=buyer_id)
        current_state = CheckNonConfirmRequestsStates.await_input_brand
    elif callback.data == 'buyer_active_offers' or current_state.startswith('CheckActiveOffersStates'):
        ic()
        current_brands = await offer_requester_module.OffersRequester.get_for_buyer_id(buyer_id=buyer_id, get_brands=True)
        current_state = CheckActiveOffersStates.await_input_brand
    else:
        await callback.answer('В разработке')

    if not current_brands:
        if callback.data == 'return_to_choose_requests_brand':
            await buyer_offers_callback_handler(callback, state)
        elif callback.data == 'buyer_cached_offers':
            return await callback.answer(text=LEXICON["buyer_haven't_cached_requests"])
        elif callback.data == 'buyer_active_offers':
            return await callback.answer(text=LEXICON['active_offers_non_exists'])
    else:
        ic(type(current_brands))
        # await callback.message.edit_text(text=)
        await state.set_state(current_state)
        await CachedRequestsView.choose_brand_for_output(callback, car_brands=current_brands, state=state)


async def output_buyer_offers(callback: CallbackQuery, state: FSMContext):
    offer_requester_module = importlib.import_module('database.data_requests.offers_requests')
    choose_hybrid_handlers_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.hybrid_handlers')

    current_state = str(await state.get_state())
    # if callback.data.startswith('confirm_buy_settings'):
    #     advert_id =
    # else:
    car_brand = int(callback.data.split('_')[-1])
    if current_state.startswith('CheckActiveOffersStates'):
        cars = await offer_requester_module.OffersRequester.get_for_buyer_id(buyer_id=str(callback.from_user.id), brand=car_brand)
        ic()
        ic(cars)
    elif current_state.startswith('CheckNonConfirmRequestsStates'):
        cars = await offer_requester_module.CachedOrderRequests.get_cache(buyer_id=str(callback.from_user.id), brand=car_brand)
        ic(
        )
        ic(cars)
    else:
        cars = None
    if cars:
        formatted_cars_data = await choose_hybrid_handlers_module.get_cars_data_pack(callback=callback, state=state, car_models=cars)
        pagination = BuyerCarsPagination(data=formatted_cars_data, page_size=1, current_page=0)

        await pagination.send_page(request=callback, state=state)
        if current_state.startswith('CheckActiveOffersStates'):
            state_object = CheckActiveOffersStates.brand_flipping_process
        elif current_state.startswith('CheckNonConfirmRequestsStates'):
            state_object = CheckNonConfirmRequestsStates.brand_flipping_process
        else:
            state_object = None
        if state_object:
            await state.set_state(state_object)
    else:
        return_main_menu_module = importlib.import_module('handlers.callback_handlers.hybrid_part.return_main_menu')
        if current_state.startswith('CheckActiveOffersStates'):
            alert_text = LEXICON['active_offers_non_exists']
        elif current_state.startswith('CheckNonConfirmRequestsStates'):
            alert_text = LEXICON["buyer_haven't_cached_requests"]
        else:
            alert_text = None
        await callback.answer(text=alert_text)
        await return_main_menu_module.return_main_menu_callback_handler(callback, state)


