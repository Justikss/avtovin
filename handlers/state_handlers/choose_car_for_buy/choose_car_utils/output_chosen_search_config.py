import importlib
from typing import Optional, List

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.car_advert_requests import AdvertRequester
from database.data_requests.recomendations_request import RecommendationParametersBinder
from database.tables.car_configurations import CarAdvert
from database.tables.offers_history import ActiveOffers
from handlers.utils.create_advert_configuration_block import create_advert_configuration_block
from utils.get_currency_sum_usd import get_valutes


async def get_seller_header(seller=None, car=None, state=None):
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    message_text = lexicon_module.LEXICON.get('chosen_configuration').get('message_text')
    if car:
        seller = car.seller
    seller_number = ''
    if state:
        current_state = str(await state.get_state())
        if current_state.startswith('CheckActiveOffersStates'):
            seller_number = f'''{message_text.get('phone_number')}\n{seller.phone_number}'''

    if seller.dealship_name:
        seller_header = message_text.get('from_dealership').replace('X', seller.dealship_name).replace('Y', seller.dealship_address)
    else:
        seller_header = message_text.get('from_seller').replace('X', ' '.join([seller.name, seller.surname, seller.patronymic if seller.patronymic else '']))

    seller_header = f'{seller_header}{seller_number}'
    return seller_header

async def get_output_string(advert, state=None, callback=None):
    offer_requester = importlib.import_module('database.data_requests.offers_requests')
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


    if isinstance(advert, set) and len(advert) == 1:
        advert = advert.pop()
    if isinstance(advert, int | str):
        advert = await AdvertRequester.get_where_id(advert)
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

    if advert.mileage:
        mileage = advert.mileage.name
        year_of_realise = advert.year.name
    else:
        mileage, year_of_realise = None, None

    result_string = f'''{startswith_text}{seller_header}{await create_advert_configuration_block(car_state=advert.state.name, engine_type=advert.complectation.engine.name, brand=advert.complectation.model.brand.name, model=advert.complectation.model.name, complectation=advert.complectation.name, color=advert.color.name, mileage=mileage, year_of_realise=year_of_realise, sum_price=advert.sum_price, usd_price=advert.dollar_price)}{footer_viewed_by_seller_status}'''

    return result_string


async def get_cars_data_pack(callback: CallbackQuery, state: FSMContext, advert_models=None):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    cached_requests_module = importlib.import_module('database.data_requests.offers_requests')
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    redis_key = str(callback.from_user.id) + ':cars_type'
    cars_state = await redis_module.redis_data.get_data(redis_key)

    lexicon_part = lexicon_module.LEXICON.get('chosen_configuration')

    message_text = lexicon_part.get('message_text')

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


        advert_models = await AdvertRequester.get_advert_by(state_id=int(car_state),
                                                         engine_type_id=engine_type,
                                                         brand_id=brand,
                                                         model_id=model,
                                                         complectation_id=int(complectation),
                                                         color_id=color,
                                                         mileage_id=mileage,
                                                         year_of_release_id=year_of_release
                                                         )
    else:
        first_view_mode = False
    ic()
    ic(advert_models)
    if not isinstance(advert_models, list):
        advert_models = [advert_models]

    if advert_models:
        if isinstance(advert_models[0], ActiveOffers):
            data_stack = [offer_model.car_id.id for offer_model in advert_models]
        # elif isinstance(advert_models, int):
        #     advert_models = await AdvertRequester.get_where_id(advert_models)
    else:
        return False

    if not data_stack:
        data_stack = [advert.id for advert in advert_models]
    ic(data_stack)
    if first_view_mode:
        await cached_requests_module.CachedOrderRequests.set_cache(buyer_id=callback.from_user.id, car_data=data_stack)
        await RecommendationParametersBinder.store_parameters(buyer_id=callback.from_user.id, state_id=car_state, engine_type_id=engine_type,
                                                                  complectation_id=complectation,
                                                              color_id=color, mileage_id=mileage, year_id=year_of_release)


    return data_stack


