import asyncio
import importlib
import logging

import aiohttp

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Union

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
config_module = importlib.import_module('config_data.config')

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
    async def time_endswith_fromatter(request, time_value):
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
        language = await redis_module.redis_data.get_data(
            key=f'{request.from_user.id}:language'
        )
        if language == 'ru' or language is None:
            wait_time = str(time_value)
            seconds = 'секунд'
            if wait_time[-1] == '1' and wait_time != '11':
                seconds += Lexicon_module.SecondsEndswith.one
            elif 1 < int(wait_time[-1]) <= 4:
                seconds += Lexicon_module.SecondsEndswith.two_four
            else:
                pass
        else:
            seconds = 'soniya'

        return seconds



    @staticmethod
    async def get_address_from_locationiq(latitude, longitude):
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

        # await redis_module.redis_data.delete_key(key=f'{latitude},{longitude}')
        cached_result = await redis_module.redis_data.get_data(key=f'{latitude},{longitude}')
        if cached_result:
            return cached_result
        url = f"https://us1.locationiq.com/v1/reverse.php?key={config_module.LOCATIONIQ_TOKEN}&lat={latitude}&lon={longitude}&format=json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    address = await GetDealershipAddress.format_address(data.get("display_name"))
                    await redis_module.redis_data.set_data(key=f'{latitude},{longitude}', value=address,
                                                           expire=config_module.geolocation_cahce_expire)
                    return address
                else:
                    logging.critical('Не удалось провести запрос к locationiq.\nСтатус код: %d', response.status)

    @staticmethod
    async def process_queue():
        while True:
            lat, lon, result_future = await queue.get()
            address = await GetDealershipAddress.get_address_from_locationiq(lat, lon)
            if address:
                result_future.set_result(address)
            else:
                from utils.lexicon_utils.Lexicon import LEXICON
                result_future.set_result(LEXICON['address_was_not_found'])
            await asyncio.sleep(1)  # Задержка между запросами

    async def __call__(self, request: Union[Message, CallbackQuery], state: FSMContext):
        message_editor_module = importlib.import_module('handlers.message_editor')
        input_dealship_name_module = importlib.import_module('handlers.state_handlers.seller_states_handler.seller_registration.seller_registration_handlers')
        if isinstance(request, Message):
            if request.location:
                lat = request.location.latitude
                lon = request.location.longitude
                wait_time = queue.qsize()  # Расчет времени ожидания
                if int(wait_time) > 3:
                    seconds_endswith = await GetDealershipAddress.time_endswith_fromatter(request, wait_time)
                    lexicon_part = f'''{Lexicon_module.LEXICON['waiting_request_process'].format(time=wait_time, seconds=seconds_endswith)}.'''
                    await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part)

                result_future = asyncio.get_running_loop().create_future()
                await queue.put((lat, lon, result_future))
                address = await result_future
                return {'dealership_address': address}
            else:
                dealership_address = request.text.strip()
                if len(dealership_address) < config_module.max_contact_info_len:
                    for symbol in request.text:
                        if symbol.isalpha():
                            return {'dealership_address': request.text}
                await input_dealship_name_module.dealership_input_address(request=request, state=state, incorrect='(novalid)')
        else:
            return True
