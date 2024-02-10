import asyncio

import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Location
from icecream import ic

from tests.test_aiogram.utils import get_message


# @pytest.mark.asyncio
# async def test_call_method(dispatcher, bot, state):
#     from tests.test_aiogram.test_get_dealership_adress import GetDealershipAddress
#     # Мокаем необходимые вызовы
#     event_loop = asyncio.get_running_loop()
#     event_loop.create_task(GetDealershipAddress.process_queue(state))
#     # with patch('tests.test_aiogram.test_get_dealership_adress.GetDealershipAddress.process_queue'):
#     message = get_message(location=Location(latitude=48.8584, longitude=2.2945))  # Пример координат
#     # GetDealershipAddress.get_address_from_locationiq = AsyncMock(return_value="Some Address")
#
#     # Вызываем метод
#     filter_instance = GetDealershipAddress()
#     result = await filter_instance(message, state)
#
#     # Проверяем результат
#     ic(result)
#     assert result != {'dealership_address': "address_was_not_found"}
#     # event_loop.close()
#     await dispatcher.emit_shutdown()
#     for task in asyncio.all_tasks():
#         task.cancel()
#         try:
#             await task
#         except asyncio.CancelledError:
#             pass



@pytest.mark.asyncio
async def test_queue_processing_and_address_accuracy(dispatcher, state):
    from tests.test_aiogram.test_get_dealership_adress import GetDealershipAddress, queue
    event_loop = asyncio.get_running_loop()

    event_loop.create_task(GetDealershipAddress.process_queue(state))

    address_filter = GetDealershipAddress()

    # Координаты и ожидаемые подстроки в ответе
    test_data = [
        (48.8584, 2.2945, ['Eiffel', 'Paris']),   # Эйфелева башня, Париж
        (40.7128, -74.0060, ['New York']),         # Нью-Йорк
        (55.7558, 37.6176, ['Moscow', 'Kremlin']), # Москва, Кремль
        (35.6895, 139.6917, ['Tokyo']),            # Токио
        (51.5074, -0.1278, ['London']),            # Лондон
        (28.6139, 77.2090, ['Delhi']),             # Нью-Дели
        # (34.0522, -118.2437, ['Los Angeles']),     # Лос-Анджелес
        # (41.9028, 12.4964, ['Rome']),              # Рим
        # (33.8688, 151.2093, ['Sydney']),           # Сидней
        # (22.9068, -43.1729, ['Rio']),               # Рио-де-Жанейро
        (48.8584, 2.2945, ['Eiffel', 'Paris']),  # Эйфелева башня, Париж
        (40.7128, -74.0060, ['New York']),  # Нью-Йорк
        (55.7558, 37.6176, ['Moscow', 'Kremlin']),  # Москва, Кремль
        (35.6895, 139.6917, ['Tokyo']),  # Токио
        (51.5074, -0.1278, ['London']),  # Лондон
        (28.6139, 77.2090, ['Delhi']),  # Нью-Дели
#         (34.0522, -118.2437, ['Los Angeles']),  # Лос-Анджелес
#         (41.9028, 12.4964, ['Rome']),  # Рим
#         (33.8688, 151.2093, ['Sydney']),  # Сидней
#         (22.9068, -43.1729, ['Rio'])  # Рио-де-Жанейро
    ]
    # Создание асинхронных задач для каждого запроса
    tasks = []
    for lat, lon, _ in test_data:
        message = get_message(location=Location(latitude=lat, longitude=lon))
        task = event_loop.create_task(address_filter(message, state))
        tasks.append(task)

    # Ожидание выполнения всех задач
    responses = await asyncio.gather(*tasks)
    # Проверка результатов
    for i, response in enumerate(responses):
        current_queue_size = queue.qsize()
        expected_substrings = test_data[i][2]

        ic(response, expected_substrings, any(substring in response['dealership_address'] for substring in expected_substrings))

        # ic(current_queue_size)
        # if current_queue_size > 3:
        #     assert str(current_queue_size) in response['dealership_address']
        # else:
        assert any(substring in response['dealership_address'] for substring in expected_substrings) or 'address_was_not_found' not in response['dealership_address']

    await dispatcher.emit_shutdown()
    for task in asyncio.all_tasks():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

