import importlib
from copy import copy

from database.tables.car_configurations import CarColor, CarAdvert
from database.tables.statistic_tables.advert_parameters import AdvertParameters
from utils.get_currency_sum_usd import get_valutes
# from  import LexiconSellerRequests as Lexicon

lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def to_ru(element, language):
    ru_language = language == 'ru'
    return element.name_ru if element.name_ru and ru_language else element.name

async def create_advert_configuration_block(car_state=None, engine_type=None, brand=None, model=None, complectation=None, color=None, sum_price=None, usd_price=None, year_of_realise=None, mileage=None, advert_id=None, language=None):
    # configurate_block = f'''{copy(Lexicon.commodity_output_block).replace('SN', car_state).replace('EN', engine_type).replace('BN', brand).replace('MN', model).replace('COMPN', complectation).replace('COLN', color).replace('YV', str(year_of_realise)).replace('MV', str(mileage))}'''
    if advert_id:
        advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')
        if not isinstance(advert_id, (CarAdvert, AdvertParameters)):
            if not isinstance(advert_id, int):
                advert_id = int(advert_id)
            advert_model = await advert_requests_module.AdvertRequester.get_where_id(advert_id)
        else:
            advert_model = advert_id
        engine_type = await to_ru(advert_model.complectation.engine, language)
        brand = advert_model.complectation.model.brand.name
        model = advert_model.complectation.model.name
        complectation = await to_ru(advert_model.complectation, language)
        color = await to_ru(advert_model.color, language)
        sum_price = advert_model.sum_price if hasattr(advert_model, 'sum_price') else None
        usd_price = advert_model.dollar_price if hasattr(advert_model, 'dollar_price') else None
        if (sum_price or usd_price):
            year_of_realise = advert_model.year
            mileage = advert_model.mileage
            car_state = await to_ru(advert_model.state, language)

    ic(isinstance(color, CarColor))
    ic(color)

    if language == 'ru':
        lexicon = copy(lexicon_module\
                        .lexicon_ru['commodity_output_block'])
    else:
        lexicon = copy(lexicon_module\
                             .LexiconSellerRequests.commodity_output_block)

    configurate_block = copy(lexicon).format(state=car_state, engine_type=engine_type,
                                            brand_name=brand, model_name=model,
                                            complectation=complectation, year_of_release=year_of_realise,
                                            mileage=mileage, color=color)
    ic(configurate_block)
    ic(configurate_block.split('\n'))
    if 'None' in configurate_block:
        configurate_block = '\n'.join([part.strip() for part in configurate_block.split('\n') if ('None' not in part) and part.strip()])

    configurate_block = f'''\n{configurate_block}'''
    ic(configurate_block)

    ic(sum_price, usd_price)
    if sum_price or usd_price:
        configurate_block += f'''\n{await get_valutes(usd=usd_price, sum_valute=sum_price, get_string='block', language=language)}'''
    ic(configurate_block)

    if not car_state:
        configurate_block = configurate_block.split('\n')
        configurate_block[2] = f'<blockquote>{configurate_block[2]}'
        configurate_block = '\n'.join(configurate_block)

    ic(configurate_block)

    return configurate_block