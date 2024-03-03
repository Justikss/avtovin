import logging
import os
import traceback

from dotenv import find_dotenv, load_dotenv
from icecream import ic
from peewee import SqliteDatabase, Model, TextField, CharField, IntegerField, ForeignKeyField, AutoField
from peewee_async import PooledPostgresqlDatabase, Manager

from database.triggers import create_trigger_unique_phone_number


if not find_dotenv():
    exit("Переменные окружения для базы данных не загружены т.к отсутствует файл database/.env")
else:
    load_dotenv('database/.env')

connect_data = {
    'database': os.getenv('database'),
'user': os.getenv('user'),
'password': os.getenv('password'),
'host': os.getenv('host'),
'port': os.getenv('port')
}

connect_dataa = {
    'database': 'testDB',
'user': 'postgres',
'password': 'red12red1212',
'host': 'localhost',
'port': 5432
}

database = PooledPostgresqlDatabase(
    connect_data['database'],
    user=connect_data['user'],
    password=connect_data['password'],
    host=connect_data['host'],
    port=connect_data['port']
    )

class BaseModel(Model):
    class Meta:
        database = database


manager = Manager(database)



async def create_tables():
    try:
        logging.info(BaseModel.__subclasses__())
        await manager.connect()
        database.create_tables(BaseModel.__subclasses__(), safe=True)
        print('Таблицы успешно созданы')
        # try:
        #     await create_trigger_unique_phone_number(database)
        # except Exception as ex:
        #     traceback.print_exc()
        #     print(ex)

    except Exception as ex:
        traceback.print_exc()
        print(f'Ошибка при создании таблиц: {ex}, {type(ex)}')
    finally:
        await manager.close()

# def switch_database(db_config):
#     global database
#     if not db_config:
#         db_config = connect_data
#     else:
#         db_config = test_connect_data
#     database.close()
#     database.init(
#         db_config['database'],
#         user=db_config['user'],
#         password=db_config['password'],
#         host=db_config['host'],
#         port=db_config['port']
#     )
#     database.connect()
