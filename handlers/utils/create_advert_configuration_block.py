import importlib
from copy import copy

from database.tables.car_configurations import CarColor, CarAdvert
from utils.get_currency_sum_usd import get_valutes
from utils.lexicon_utils.Lexicon import LexiconSellerRequests as Lexicon, LEXICON


async def create_advert_configuration_block(car_state=None, engine_type=None, brand=None, model=None, complectation=None, color=None, sum_price=None, usd_price=None, year_of_realise=None, mileage=None, advert_id=None):
    # configurate_block = f'''{copy(Lexicon.commodity_output_block).replace('SN', car_state).replace('EN', engine_type).replace('BN', brand).replace('MN', model).replace('COMPN', complectation).replace('COLN', color).replace('YV', str(year_of_realise)).replace('MV', str(mileage))}'''
    if advert_id:
        advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')
        if not isinstance(advert_id, CarAdvert):
            if not isinstance(advert_id, int):
                advert_id = int(advert_id)
            advert_model = await advert_requests_module.AdvertRequester.get_where_id(advert_id)
        else:
            advert_model = advert_id
        car_state = advert_model.state.name
        engine_type = advert_model.complectation.engine.name
        brand = advert_model.complectation.model.brand.name
        model = advert_model.complectation.model.name
        complectation = advert_model.complectation.name
        color = advert_model.color.name
        sum_price = advert_model.sum_price
        usd_price = advert_model.dollar_price

    ic(isinstance(color, CarColor))
    ic(color)


    configurate_block = copy(Lexicon.commodity_output_block).format(state=car_state, engine_type=engine_type,
                                            brand_name=brand, model_name=model,
                                            complectation=complectation, year_of_release=year_of_realise,
                                            mileage=mileage, color=color)
    ic(configurate_block)
    ic(configurate_block.split('\n'))
    if 'None' in configurate_block:
        configurate_block = '\n'.join([part.strip() for part in configurate_block.split('\n') if ('None' not in part) and part.strip()])

    configurate_block = f'''\n{configurate_block}'''
    ic(configurate_block)

    configurate_block += f'''\n{await get_valutes(usd=usd_price, sum_valute=sum_price, get_string='block')}'''

    return configurate_block