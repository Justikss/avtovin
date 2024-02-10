import pytest
import pytest_asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot
import asyncio
import sys

from tests.test_aiogram.utils import TEST_USER, TEST_USER_CHAT

sys.path.insert(0, '../..')

from tests.mocked_bot import MockedBot

# @pytest.fixture(scope='module')
# async def process_queue_fixture():
#     # Запуск задачи
#     from tests.test_aiogram.test_get_dealership_adress import GetDealershipAddress
#
#     queue_task = asyncio.create_task(GetDealershipAddress.process_queue())
#
#     yield queue_task
#
#     # Отмена задачи после завершения теста
#     queue_task.cancel()
#     try:
#         await queue_task
#     except asyncio.CancelledError:
#         pass

@pytest_asyncio.fixture(scope='module')
async def storage():
    tmp_storage = MemoryStorage()
    try:
        yield tmp_storage
    finally:
        await tmp_storage.close()

@pytest.fixture(scope="module")
def bot():
    return MockedBot()


@pytest_asyncio.fixture(scope="module")
async def dispatcher(storage):
    dp = Dispatcher(storage=storage)
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


# @pytest.fixture(scope='module')
# def event_loop():
#     return asyncio.get_event_loop()


@pytest.fixture(scope='module')
def state(dispatcher: Dispatcher, bot: Bot):
    return FSMContext(dispatcher.storage, StorageKey(chat_id=TEST_USER_CHAT.id, user_id=TEST_USER.id,
                                                     bot_id=bot.id))
