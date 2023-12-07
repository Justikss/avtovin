import asyncio
import importlib
import logging
from copy import copy
from time import time
import aiohttp
import requests
from bs4 import BeautifulSoup

from utils.Lexicon import LEXICON, LexiconCommodityLoader


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


async def get_valutes(usd, sum, get_string=None):
    ic(usd, sum)

    if not usd:
        usd = await convertator('sum', sum)
    elif not sum:
        sum = await convertator('usd', usd)
    ic(usd, sum)
    usd, sum = "{:,}".format(usd), "{:,}".format(sum)
    if None not in (usd, sum):
        result = (usd, sum)
        if get_string:
            price_string = f'''{usd}$ {LEXICON['convertation_sub_string']} {LEXICON['uzbekistan_valute'].replace('X', sum)}'''
            block_string = copy(LexiconCommodityLoader.load_commodity_price['message_text']).replace('X', price_string)
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
        logging.error(f"Произошла ошибка при парсинге: {e}")
        return False

async def fetch_currency_rate():
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    while True:
        # Ваш код парсинга
        sum_currency = await currency_usd_to_sum()
        if sum_currency:
            await message_editor.redis_data.set_data(key='usd_to_sum_currency', value=sum_currency)

        # Пауза перед следующим обновлением (например, каждые 10 минут)
        await asyncio.sleep(3600)
