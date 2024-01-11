import pytest
import asyncio

from database.data_requests.statistic_requests.advert_feedbacks_requests import AdvertFeedbackRequester
from tests.tests_database.mock_connect import mock_manager

@pytest.mark.asyncio
async def test_top_advert_parameters_top():
    # Проверка корректности для топ продаваемых
    # new_loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(new_loop)

    # transaction = .database.transaction()


    top_10 = await AdvertFeedbackRequester.get_top_advert_parameters('top', mock_manager)
    # await transaction.commit()
    # ic(top_10)
    assert len(top_10) == 10
    # Дополнительные проверки на правильность ранжирования

@pytest.mark.asyncio
async def test_top_advert_parameters_bottom():
    # Проверка корректности для топ непродаваемых
    bottom_10 = await AdvertFeedbackRequester.get_top_advert_parameters('bottom', mock_manager)
#     ic(bottom_10)
    assert len(bottom_10) == 10
    # Дополнительные проверки на правильность ранжирования