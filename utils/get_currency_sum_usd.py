import asyncio
import importlib
import logging
from copy import copy
from time import time
import aiohttp
import requests
from bs4 import BeautifulSoup


excepts = 0

async def convertator(valute, cost):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    ic(valute, cost)
    sum_to_usd = await message_editor.redis_data.get_data(key='usd_to_sum_currency')

    if sum_to_usd:
        sum_to_usd = int(sum_to_usd)
        cost = int(cost)
        result = ''

        if valute == 'sum':
            result = cost / sum_to_usd
            if result >= 1:
                result = round(result)


        elif valute == 'usd':
            result = cost * sum_to_usd

        if result:
            ic(result)
            # result = "{:,}".format(result)
            return result


async def get_valutes(usd, sum_valute, get_string=None):
    ic(usd, sum_valute)
    boot_commodity_lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


    ic(sum_valute, usd)
    if not usd:
        usd = await convertator('sum', sum_valute)
    elif not sum_valute:
        sum_valute = await convertator('usd', usd)
    ic(usd, sum_valute)
    usd, sum_valute = "{:,}".format(usd), "{:,}".format(sum_valute)
    if None not in (usd, sum_valute):
        result = (usd, sum_valute)
        if get_string:
            price_string = f'''{usd}$ {lexicon_module.LEXICON['convertation_sub_string']} {lexicon_module.LEXICON['uzbekistan_valute'].replace('X', sum_valute)}'''
            block_string = copy(boot_commodity_lexicon_module.LexiconCommodityLoader.price_digital).format(price=price_string)
            if get_string == 'block':
                return block_string
            else:
                return price_string
        else:
            return result

async def currency_usd_to_sum():
    url = 'https://onmap.uz/usd'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    logging.error(f"Ошибка запроса: HTTP {response.status}")
                    return False

                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
                data = soup.find('div', class_='text-green-600 text-xl font-semibold')

                if data:
                    result = int(data.text.strip().replace('~', '').replace(' ', ''))
                    return result
                else:
                    logging.warning("Ошибка при парсинге: Данные не найдены на странице")
                    return False

    except Exception as e:
        global excepts
        logging.error(f"Произошла ошибка при парсинге: {e}")
        excepts += 1
        if excepts == 5:
            logging.critical('Five exceptions from converter parsing')
        return False

async def fetch_currency_rate():
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    while True:
        # Ваш код парсинга
        sum_currency = await currency_usd_to_sum()
        if sum_currency:
            await message_editor.redis_data.set_data(key='usd_to_sum_currency', value=sum_currency)

        await asyncio.sleep(3600)
