import pytest
import asyncio

from peewee import fn

from database.data_requests.statistic_requests.advert_feedbacks_requests import AdvertFeedbackRequester
from tests.tests_database.mock_connect import mock_manager
from tests.tests_database.mock_tables import SellerFeedbacksHistory


@pytest.mark.asyncio
async def test_top_advert_parameters_top():
    # Проверка корректности для топ продаваемых
    # new_loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(new_loop)

    # transaction = .database.transaction()


    top_10 = await AdvertFeedbackRequester.get_top_advert_parameters('top', mock_manager.database)
    # await transaction.commit()
    # ic(top_10)
    assert len(top_10) == 10
    # Дополнительные проверки на правильность ранжирования

@pytest.mark.asyncio
async def test_top_advert_parameters_bottom():
    # Проверка корректности для топ непродаваемых
    bottom_10 = await AdvertFeedbackRequester.get_top_advert_parameters('bottom', mock_manager.database)
#     ic(bottom_10)
    assert len(bottom_10) == 10
    # Дополнительные проверки на правильность ранжирования


# async def test_feedbacks_count_correct(database):
#     # Вызов вашего метода
#     feedback_statistics = await AdvertFeedbackRequester.get_top_advert_parameters('top', database)
#
#     for record in feedback_statistics:
#         # Допустим, record[1] содержит количество отзывов
#         feedbacks_count = record[1]
#
#         # Аналогично, record[0] содержит идентификатор advert_parameters
#         advert_params_id = record[0]
#
#         # Выполнение запроса для подсчета ожидаемого количества отзывов
#         # Этот запрос должен быть синхронным и соответствовать вашей базе данных
#         expected_count = your_sync_db_method_to_count_feedbacks(advert_params_id)
#
#         assert feedbacks_count == expected_count
#
# # Запуск асинхронного теста
# @pytest.mark.asyncio
# async def test_async():
#     await test_feedbacks_count_correct(mock_manager.database)