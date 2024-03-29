import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from icecream import ic

from database.tables.car_configurations import CarAdvert
from database.tables.offers_history import RecommendedOffers
from handlers.callback_handlers.buy_part.buyer_offers_branch.offers_handler import buyer_offers_callback_handler
# from handlers.callback_handlers.buy_part.main_menu import main_menu
# from handlers.callback_handlers.hybrid_part.return_main_menu import return_main_menu_callback_handler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_cars_pagination_system.pagination_system_for_buyer import \
    BuyerCarsPagination
from states.buyer_offers_states import CheckNonConfirmRequestsStates, CheckActiveOffersStates, \
    CheckRecommendationsStates

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
recomendations_request_module = importlib.import_module('database.data_requests.recomendations_request')


async def buyer_get_requests__chose_brand(callback: CallbackQuery, state: FSMContext):
    offer_requester_module = importlib.import_module('database.data_requests.offers_requests')

    buyer_id = str(callback.from_user.id)
    current_brands = None
    current_state = str(await state.get_state())
    ic(callback.data, current_state)

    if callback.data == 'buyer_cached_offers' or (current_state.startswith('CheckNonConfirmRequestsStates') or
                                                  current_state == 'CheckActiveOffersStates:show_from_non_confirm_offers'):
        current_brands = await offer_requester_module.CachedOrderRequests.get_cache(buyer_id=buyer_id, get_brands=True)
        current_state = CheckNonConfirmRequestsStates.await_input_brand
        non_exists_alert_text = Lexicon_module.LEXICON["buyer_haven't_cached_requests"]

    elif callback.data == 'buyers_recommended_offers' or (current_state.startswith('CheckRecommendationsStates') or
                                                          current_state == 'CheckActiveOffersStates:show_from_recommendates'):
        current_brands = await recomendations_request_module\
            .RecommendationRequester.retrieve_by_buyer_id(buyer_id, get_brands=True)
        current_state = CheckRecommendationsStates.await_input_brand
        non_exists_alert_text = Lexicon_module.LEXICON['buyer_havent_recommendated_offers']
    elif callback.data == 'buyer_active_offers' or current_state.startswith('CheckActiveOffersStates'):
        current_brands = await offer_requester_module.OffersRequester.get_for_buyer_id(buyer_id=buyer_id, get_brands=True)
        current_state = CheckActiveOffersStates.await_input_brand
        non_exists_alert_text = Lexicon_module.LEXICON['active_offers_non_exists']

    else:
        non_exists_alert_text = None
        # await callback.answer('В разработке')
    ic(current_brands)#, current_brands[0].__dict__)
    if not current_brands:
        ic()
        if non_exists_alert_text:
            await callback.answer(non_exists_alert_text)
        if callback.data == 'return_to_choose_requests_brand':
            await buyer_offers_callback_handler(callback, state, delete_mode=True)
        return
    else:
        inline_buttons_pagination_heart_module = importlib.import_module('handlers.utils.inline_buttons_pagination_heart')
        ic(current_brands)
        current_brands = {
            f'load_brand_{str(brand.id)}': brand.name
            for brand in current_brands}

        ic(type(current_brands))
        ic(current_brands)
        # await callback.message.edit_text(text=)
        await state.set_state(current_state)
        await inline_buttons_pagination_heart_module.CachedRequestsView.output_message_with_inline_pagination(
            callback, buttons_data=current_brands, state=state, pagesize=8
        )


async def output_buyer_offers(callback: CallbackQuery, state: FSMContext):
    offer_requester_module = importlib.import_module('database.data_requests.offers_requests')
    choose_hybrid_handlers_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.hybrid_handlers')

    current_state = str(await state.get_state())
    ic(current_state)
    buyer_id = int(callback.from_user.id)
    # if callback.data.startswith('confirm_buy_settings'):
    #     advert_id =
    # else:
    adverts = None
    offers = None
    advert_ids = None

    car_brand = int(callback.data.split('_')[-1])
    if current_state.startswith('CheckActiveOffersStates'):
        offers = await offer_requester_module.OffersRequester.get_for_buyer_id(buyer_id=buyer_id, brand=car_brand)
        state_object = CheckActiveOffersStates.brand_flipping_process
        non_exists_alert_text = Lexicon_module.LEXICON['active_offers_non_exists']

    elif current_state.startswith('CheckNonConfirmRequestsStates'):
        offers = await offer_requester_module.CachedOrderRequests.get_cache(buyer_id=buyer_id, brand=car_brand)
        state_object = CheckNonConfirmRequestsStates.brand_flipping_process
        non_exists_alert_text = Lexicon_module.LEXICON["buyer_haven't_cached_requests"]
    elif current_state.startswith('CheckRecommendationsStates'):
        offers = await recomendations_request_module\
            .RecommendationRequester.retrieve_by_buyer_id(buyer_id=buyer_id, by_brand=car_brand)
        state_object = CheckRecommendationsStates.brand_flipping_process
        non_exists_alert_text = Lexicon_module.LEXICON['buyer_havent_recommendated_offers']
    else:
        state_object = None
        non_exists_alert_text = None
    ic(offers, adverts)
    if offers:
        advert_ids = []
        for offer in offers:
            if isinstance(offer, RecommendedOffers):
                advert_id = offer.advert.id
            # elif isinstance(offer, CarAdvert):
            #     advert_id = offer.id
            else:
                advert_id = offer.car_id.id

            ic(advert_id)
            advert_ids.append(advert_id)
            ic(advert_ids)

    elif adverts:
        advert_ids = [advert.id for advert in adverts]

    if advert_ids:
        pagination = BuyerCarsPagination(data=advert_ids, page_size=1, current_page=0)
        await pagination.send_page(request=callback, state=state)

        if state_object:
            await state.set_state(state_object)
    else:
        return_main_menu_module = importlib.import_module('handlers.callback_handlers.hybrid_part.return_main_menu')
        await callback.answer(text=non_exists_alert_text)
        await return_main_menu_module.return_main_menu_callback_handler(callback, state)


