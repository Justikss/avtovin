from aiogram.types import Message

from database.data_requests.car_configurations_requests import mock_values
from database.data_requests.utils.drop_tables import drop_tables_except_one
from database.db_connect import create_tables


async def drop_table_handler(message: Message):
    await drop_tables_except_one('Фотографии_Новых_Машин')
    await create_tables()
    await mock_values()
    await message.answer('SUCCESS')