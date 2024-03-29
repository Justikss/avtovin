import importlib
from copy import copy

from database.tables.car_configurations import CarColor, CarAdvert
from database.tables.statistic_tables.advert_parameters import AdvertParameters
from utils.get_currency_sum_usd import get_valutes
# from  import LexiconSellerRequests as Lexicon

lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def to_language(element, language):
    result = ''
    ic()
    ic(element, language)
    name_on_language = f'name_{language}'
    ic(name_on_language)
    ic(hasattr(element, name_on_language))
    if hasattr(element, name_on_language):
        result = getattr(element, name_on_language)
    ic()
    ic(result)
    if not result:
        result = element.name
    ic(result)

    return result


async def create_advert_configuration_block(car_state=None, engine_type=None, brand=None, model=None, complectation=None, color=None, sum_price=None, usd_price=None, year_of_realise=None, mileage=None, advert_id=None, language=None):
    # configurate_block = f'''{copy(Lexicon.commodity_output_block).replace('SN', car_state).replace('EN', engine_type).replace('BN', brand).replace('MN', model).replace('COMPN', complectation).replace('COLN', color).replace('YV', str(year_of_realise)).replace('MV', str(mileage))}'''
    if advert_id:
        advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')
        if not isinstance(advert_id, (CarAdvert, AdvertParameters)):
            if not isinstance(advert_id, int):
                advert_id = int(advert_id)
            advert_model = await advert_requests_module.AdvertRequester.get_where_id(advert_id=advert_id)
        else:
            advert_model = advert_id
        # ic(lan)
        ic(advert_model)
        ic()
        engine_type = await to_language(advert_model.complectation.engine, language)
        brand = advert_model.complectation.model.brand.name
        model = advert_model.complectation.model.name
        complectation = await to_language(advert_model.complectation, language)
        color = await to_language(advert_model.color, language)
        sum_price = advert_model.sum_price if hasattr(advert_model, 'sum_price') else None
        usd_price = advert_model.dollar_price if hasattr(advert_model, 'dollar_price') else None
        if (sum_price or usd_price):
            if advert_model.year and advert_model.mileage:
                year_of_realise = advert_model.year.name
                mileage = advert_model.mileage.name
            else:
                year_of_realise = None
                mileage = None
            car_state = await to_language(advert_model.state, language)

    ic(isinstance(color, CarColor))
    ic(color)
    ic()
    ic(language)
    if language:

        lexicon = copy(lexicon_module\
                        .class_lexicon._data)[language]['commodity_output_block']
    else:
        lexicon = copy(lexicon_module\
                             .LexiconSellerRequests.commodity_output_block)
        from utils.safe_dict_class import current_language
        ic(current_language.get())

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