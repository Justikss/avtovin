from . import commodity, offers_history, seller, user, tariff, car_configurations, admin, statistic_tables
# from .start_tables import BaseModel, database
#
# manager = Manager(database)
#
# async def create_tables():
#     try:
#         print(BaseModel.__subclasses__())
#         await manager.connect()
#         await database.create_tables(BaseModel.__subclasses__(), safe=True)
#         print('Таблицы успешно созданы')
#     except Exception as ex:
#         print(f'Ошибка при создании таблиц: {ex}, {type(ex)}')
#     finally:
#         await manager.close()