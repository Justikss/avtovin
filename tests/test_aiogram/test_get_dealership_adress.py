import asyncio
import logging
import os
from unittest.mock import patch, AsyncMock

import aiohttp

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Union

from icecream import ic
from dotenv import load_dotenv

load_dotenv()
LOCATIONIQ_TOKEN = os.getenv("LOCATIONIQ_TOKEN")
queue = asyncio.Queue()

class GetDealershipAddress(BaseFilter):
    @staticmethod
    async def format_address(raw_result):
        parts = raw_result.split(', ')
        if len(parts) >= 3:
            house_number = parts[0]
            street = parts[1]
            city = parts[3]
            # full_city = parts[4]
            result = f'{city}, {street} {house_number}'
        else:
            result = raw_result

        return result

    @staticmethod
    async def time_endswith_fromatter(request, state: FSMContext, time_value):
        memory_storage = await state.get_data()
        language = memory_storage.get(
            f'{request.from_user.id}:language'
        )
        if language == 'ru' or language is None:
            wait_time = str(time_value)
            seconds = 'секунд'
            if wait_time[-1] == '1' and wait_time != '11':
                seconds += 'а'
            elif 1 < int(wait_time[-1]) <= 4:
                seconds += 'ы'
            else:
                pass
        else:
            seconds = 'soniya'

        return seconds



    @staticmethod
    async def get_address_from_locationiq(latitude, longitude, state: FSMContext):
        memory_storage = await state.get_data()
        cached_result = memory_storage.get(f'{latitude},{longitude}')
        if cached_result:
            return cached_result
        url = f"https://us1.locationiq.com/v1/reverse.php?key={LOCATIONIQ_TOKEN}&lat={latitude}&lon={longitude}&format=json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                ic(response.status)
                # ic(LOCATIONIQ_TOKEN)

                if response.status == 200:
                    data = await response.json()
                    ic(data.get("display_name"))
                    address = await GetDealershipAddress.format_address(data.get("display_name"))
                    memory_storage[f'{latitude},{longitude}'] = address
                    await state.set_data(memory_storage)
                    return address
                else:
                    headers = response.headers
                    body = await response.text()
                    print('+' * 50)
                    ic(headers, body, url)
                    print('+' * 50)

                    logging.critical('Не удалось провести запрос к locationiq.\nСтатус код: %d', response.status)

    @staticmethod
    async def process_queue(state: FSMContext):
        while True:
            lat, lon, result_future = await queue.get()
            address = await GetDealershipAddress.get_address_from_locationiq(lat, lon, state)
            if address:
                result_future.set_result(address)
            else:
                result_future.set_result('address_was_not_found')
            await asyncio.sleep(1)  # Задержка между запросами

    async def __call__(self, request: Union[Message, CallbackQuery], state: FSMContext):
        if isinstance(request, Message):
            if request.location:
                lat = request.location.latitude
                lon = request.location.longitude
                wait_time = queue.qsize()  # Расчет времени ожидания
                if int(wait_time) > 3:
                    seconds_endswith = await GetDealershipAddress.time_endswith_fromatter(request, state, wait_time)
                    lexicon_part = f'''waiting_request_process {wait_time, seconds_endswith}.'''
                    ic(lexicon_part)

                result_future = asyncio.get_running_loop().create_future()
                await queue.put((lat, lon, result_future))
                address = await result_future
                ic(address)
                # ic(address())
                return {'dealership_address': address}
            else:
                dealership_address = request.text.strip()
                if len(dealership_address) < 100:
                    for symbol in request.text:
                        if symbol.isalpha():
                            return {'dealership_address': request.text}
                return '(novalid)'
        else:
            return True
