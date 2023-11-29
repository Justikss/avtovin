from peewee import SqliteDatabase, Model, TextField, CharField, IntegerField, ForeignKeyField, AutoField
from peewee_async import PooledPostgresqlDatabase, Manager



database = PooledPostgresqlDatabase(
    'postgres',
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

    except Exception as ex:
        print(f'Ошибка при создании таблиц: {ex}, {type(ex)}')
    finally:
        await manager.close()
