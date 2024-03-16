import asyncio
import importlib

import peewee_async
from peewee import Model
from peewee_async import Manager


import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# 1. Создание тестовой базы данных в PostgreSQL (предполагается, что она уже создана)

# 2. Настройка соединения с тестовой базой данных
mock_database = peewee_async.PooledPostgresqlDatabase(
    'TestDB',
    user='postgres',
    password='red12red1212',
    host='localhost',
    port=5432
    )

mock_manager = Manager(mock_database)
class TestModel(Model):
    """Базовый класс модели для тестовой базы данных."""
    class Meta:
        database = mock_database


async def create_tables_and_insert_mock_data():
    mock_data_module = importlib.import_module('tests.tests_database.mock_data')

    # Создание таблиц
    mock_database.connect()
    mock_database.create_tables(TestModel.__subclasses__(), safe=True)

    mock_database.close()
    await mock_data_module.generate_mock_data(mock_manager, mock_database)

loop = asyncio.get_event_loop()
loop.run_until_complete(create_tables_and_insert_mock_data())
# loop.close()