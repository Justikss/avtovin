import traceback

from peewee import SqliteDatabase, Model, TextField, CharField, IntegerField, ForeignKeyField, AutoField
from peewee_async import PooledPostgresqlDatabase, Manager

from database.triggers import create_trigger_unique_phone_number

database = PooledPostgresqlDatabase(
    'postgresDB',
    user='postgres',
    password='red12red1212',
    host='localhost',
    port=5432
    )

class BaseModel(Model):
    class Meta:
        database = database


manager = Manager(database)



async def create_tables():
    try:
        print(BaseModel.__subclasses__())
        await manager.connect()
        database.create_tables(BaseModel.__subclasses__(), safe=True)
        print('Таблицы успешно созданы')
        # try:
        #     await create_trigger_unique_phone_number(database)
        # except Exception as ex:
        #     traceback.print_exc()
        #     print(ex)

    except Exception as ex:
        print(f'Ошибка при создании таблиц: {ex}, {type(ex)}')
    finally:
        await manager.close()
