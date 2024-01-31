import importlib
from copy import copy

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.utils.create_advert_configuration_block import create_advert_configuration_block


car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')
offers_history_module = importlib.import_module('database.tables.offers_history')

async def get_seller_header(seller=None, car=None, state=None, language=None):
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    ic()
    ic(car)
    if language == 'ru':
        message_text = copy(lexicon_module.__LEXICON).get('chosen_configuration').get('message_text')
    else:
        message_text = lexicon_module.LEXICON.get('chosen_configuration').get('message_text')
    if car:
        seller = car.seller
        ic()
        ic(seller, car.seller)
    seller_number = ''
    if state:
        current_state = str(await state.get_state())
        if current_state.startswith('CheckActiveOffersStates'):
            seller_number = f'''{message_text.get('phone_number')}\n{seller.phone_number}'''

    if seller.dealship_name:
        seller_header = message_text.get('from_dealership').format(dealership_name=seller.dealship_name, dealership_address=seller.dealship_address)
    else:
        seller_header = message_text.get('from_seller').format(seller_name=' '.join([seller.surname, seller.name, seller.patronymic if seller.patronymic else '']))

    seller_header = f'{seller_header}{seller_number}'
    return seller_header

async def get_output_string(advert, state=None, callback=None):
    offer_requester = importlib.import_module('database.data_requests.offers_requests')
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    ic(advert)
    ic()

    if isinstance(advert, set) and len(advert) == 1:
        advert = advert.pop()
    if isinstance(advert, int | str):
        advert = await car_advert_requests_module\
            .AdvertRequester.get_where_id(advert_id=advert)
    seller_header = await get_seller_header(car=advert, state=state)
    footer_viewed_by_seller_status = ''

    if state:
        current_state = str(await state.get_state())
        ic(current_state)
        if current_state.startswith('CheckActiveOffersStates'):
            startswith_text = f'''{lexicon_module.LEXICON['active_offer_caption']}\n'''
            if callback:
                offer_model = await offer_requester.OffersRequester.get_offer_model(int(callback.from_user.id), advert.id)
                if offer_model:
                    viewed_status_lexicon = lexicon_module.LEXICON["footer_for_output_active_offers"]
                    footer_viewed_by_seller_status = f'''\n\n{viewed_status_lexicon['viewed_status']}\n{viewed_status_lexicon['status_true'] if offer_model.viewed else viewed_status_lexicon['status_false']}'''
        elif current_state.startswith('CheckRecommendationsStates'):
            startswith_text = f'''{lexicon_module.LEXICON['new_recommended_offer_startswith']}\n'''
        # elif current_state.startswith('HybridChooseStates'):
        else:
            startswith_text = ''

    from database.data_requests.car_advert_requests import AdvertRequester
    await AdvertRequester.load_related_data_for_advert(advert)

    if advert.mileage:
        mileage = advert.mileage.name
        year_of_realise = advert.year.name
    else:
        mileage, year_of_realise = None, None

    result_string = f'''{startswith_text}{seller_header}{await create_advert_configuration_block(car_state=advert.state.name, engine_type=advert.complectation.engine.name, brand=advert.complectation.model.brand.name, model=advert.complectation.model.name, complectation=advert.complectation.name, color=advert.color.name, mileage=mileage, year_of_realise=year_of_realise, sum_price=advert.sum_price, usd_price=advert.dollar_price)}{footer_viewed_by_seller_status}'''

    return result_string


async def get_cars_data_pack(callback: CallbackQuery, state: FSMContext, advert_models=None, cost_filter=None):
    # redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    cached_requests_module = importlib.import_module('database.data_requests.offers_requests')
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    redis_key = str(callback.from_user.id) + ':cars_type'
    # cars_state = await redis_module.redis_data.get_data(redis_key)

    lexicon_part = lexicon_module.LEXICON.get('chosen_configuration')

#     message_text = lexicon_part.get('message_text')

    data_stack = []
    ic()
    ic(advert_models)
    if not advert_models:
        first_view_mode = True
        memory_storage = await state.get_data()
        ic(memory_storage)

        car_state = memory_storage.get('cars_state')
        brand = memory_storage.get('cars_brand')
        model = memory_storage.get('cars_model')
        engine_type = memory_storage.get('cars_engine_type')
        year_of_release = memory_storage.get('cars_year_of_release')
        mileage = memory_storage.get('cars_mileage')
        color = memory_storage.get('cars_color')
        complectation = str(memory_storage.get('cars_complectation'))
        ic(car_state)

        if str(complectation).isdigit():
            complectation = int(complectation)

        advert_models = await car_advert_requests_module\
            .AdvertRequester.get_advert_by(state_id=int(car_state),
                                                         engine_type_id=engine_type,
                                                         brand_id=brand,
                                                         model_id=model,
                                                         complectation_id=complectation,
                                                         color_id=color,
                                                         mileage_id=mileage,
                                                         year_of_release_id=year_of_release,
                                                         buyer_search_mode=callback.from_user.id,
                                                         cost_filter=cost_filter)
        ic(len(advert_models))
        if advert_models and not cost_filter:
            await collect_usd_price_diapason(advert_models, state)

    else:
        first_view_mode = False
    ic()
    ic(advert_models)
    if not isinstance(advert_models, list):
        advert_models = [advert_models]

    if advert_models:
        if isinstance(advert_models[0], offers_history_module\
                .ActiveOffers):
            data_stack = [offer_model.car_id.id for offer_model in advert_models]

    else:
        return False

    if not data_stack:
        data_stack = [advert.id for advert in advert_models]
    ic(data_stack, first_view_mode)
    if first_view_mode:
        from database.data_requests.recomendations_request import RecommendationParametersBinder

        await cached_requests_module.CachedOrderRequests.set_cache(buyer_id=callback.from_user.id, car_data=data_stack)
        await RecommendationParametersBinder.store_parameters(buyer_id=callback.from_user.id,
                                                              complectation_id=complectation,
                                                              color_id=color,
                                                              model=model)


    return data_stack

async def collect_usd_price_diapason(adverts, state):
    # ic(advert_models[0].__dict__)
    prices = set()
    for advert_model in adverts:
        usd_price = advert_model.dollar_price
        sum_price = advert_model.sum_price
        if sum_price and not usd_price:
            from utils.get_currency_sum_usd import convertator
            usd_price = await convertator('sum', sum_price)
        prices.add(usd_price)

    prices = list(prices)


    default_costs_diapason_on_buy_search = {'from': min(prices), 'before': max(prices)}
    await state.update_data(all_usd_prices=prices)
    await state.update_data(default_costs_diapason_on_buy_search=default_costs_diapason_on_buy_search)