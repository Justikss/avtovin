from copy import copy

from database.tables.car_configurations import CarColor
from utils.get_currency_sum_usd import get_valutes
from utils.lexicon_utils.Lexicon import LexiconSellerRequests as Lexicon, LEXICON


async def create_advert_configuration_block(car_state, engine_type, brand, model, complectation, color, sum_price, usd_price, year_of_realise=None, mileage=None):
    # configurate_block = f'''{copy(Lexicon.commodity_output_block).replace('SN', car_state).replace('EN', engine_type).replace('BN', brand).replace('MN', model).replace('COMPN', complectation).replace('COLN', color).replace('YV', str(year_of_realise)).replace('MV', str(mileage))}'''
    ic(isinstance(color, CarColor))
    ic(color)
    # if isinstance(color, CarColor):
    #     color = color.name
    # elif color is None:
    #     color = LEXICON['other_caption']
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