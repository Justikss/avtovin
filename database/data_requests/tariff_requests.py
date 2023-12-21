from typing import Union, List

from database.tables.tariff import Tariff, TariffsToSellers
from utils.custom_exceptions.database_exceptions import TariffHasClientsException
from database.db_connect import database, manager



class TarifRequester:
    @staticmethod
    async def retrieve_all_data() -> Union[bool, List[Tariff]]:
        '''Асинхронный метод для извлечения всех моделей тарифов'''
        query = Tariff.select()
        select_request = await manager.execute(query)
        return list(select_request) if select_request else False

    @staticmethod
    async def set_tariff(data: dict) -> bool:
        '''Асинхронный метод для установки тарифа'''
        try:
            insert_query = Tariff.insert(**data)
            await manager.execute(insert_query)
            return True
        except Exception as ex:
            print(ex)
            return False

    @staticmethod
    async def get_by_id(tariff_id):
        '''Асинхронный метод получения тарифа по ID'''
        if not isinstance(tariff_id, int):
            tariff_id = int(tariff_id)
        try:
            tariff = await manager.get(Tariff, Tariff.id == tariff_id)
        except:
            tariff = None
        return tariff

    @staticmethod
    async def get_by_name(tariff_name: str):
        '''Асинхронный метод получения тарифа по имени'''
        query = Tariff.select().where(Tariff.name == tariff_name)
        select_response = await manager.execute(query)
        return list(select_response) if select_response else False

    @staticmethod
    async def delete_tariff(tariff_name: str) -> bool:
        '''Асинхронный метод удаления тарифа'''
        try:
            tariff_model = await database.get(Tariff, Tariff.name == tariff_name)
            if tariff_model and not await manager.execute(TariffsToSellers.select().where(TariffsToSellers.tariff == tariff_model)):
                delete_query = Tariff.delete().where(Tariff.id == tariff_model.id)
                await manager.execute(delete_query)
                return True
            else:
                return False
        except Exception as ex:
            print(ex)
            return False


data = {'name': 'minimum',
'price': 50,
'duration_time': '365',
'feedback_amount': 100}

data2 = {'name': 'medium',
'price': 200,
'duration_time': '365',
'feedback_amount': 500}

data3 = {'name': 'maximum',
'price': 1000,
'duration_time': '365',
'feedback_amount': 10000}

# TarifRequester.set_tariff(data)
# TarifRequester.set_tariff(data3)
# TarifRequester.set_tariff(data2)
