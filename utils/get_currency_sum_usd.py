import asyncio
import importlib
import logging
from time import time
import aiohttp
import requests
from bs4 import BeautifulSoup

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
