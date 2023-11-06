from typing import Union, List

from database.tables.start_tables import db
from database.tables.tariff import Tariff, TariffsToSellers
from utils.custom_exceptions.database_exceptions import TariffHasClientsException

class TarifRequester:
    @staticmethod
    def retrieve_all_data() -> Union[bool, List[Tariff]]:
        '''Извлечь все модели тарифов'''

        with db.atomic():     
            select_request = Tariff.select()

        if list(select_request):
            return list(select_request)
        else:
            return False

    @staticmethod
    def set_tariff(data: dict):
        with db.atomic():
            try:
                select_response = Tariff.insert(**data).execute()

                return True
            except Exception as ex:
                print(ex)
                return False

    @staticmethod
    def get_by_id(tariff_id):
        with db.atomic():
            query = Tariff.get_by_id(tariff_id)
            return query
    
    @staticmethod
    def get_by_name(tariff_name: str):
        with db.atomic():
            try:
                print('trfn: ', tariff_name)
                select_response = Tariff.select().where(Tariff.name == tariff_name)
                print(select_response)
                select_response = list(select_response)
                return select_response
            except Exception as ex:
                print(ex)
            
            finally:
                return False

    '''VVV В разработке VVV'''
    @staticmethod
    def delete_tariff(tariff_name: str):
        with db.atomic():
            try:
                tariff_model = Tariff.select().where(Tariff.name == tariff_name)
                if TariffsToSellers.select().where(TariffsToSellers.tariff == tariff_model):
                    #update tariff state
                    pass 
                select_response = Tariff.delete_by_id()

            except Exception as ex:
                print(ex)

data = {'name': 'minimum',
'price': 50,
'duration_time': '365:0',
'feedback_amount': 100}

data2 = {'name': 'medium',
'price': 200,
'duration_time': '365:0',
'feedback_amount': 500}

data3 = {'name': 'maximum',
'price': 1000,
'duration_time': '365:0',
'feedback_amount': 10000}

# TarifRequester.set_tariff(data)
# TarifRequester.set_tariff(data3)
# TarifRequester.set_tariff(data2)
