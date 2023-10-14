from typing import Union, List

from database.tables.commodity import Commodity
from database.tables.start_tables import db


class CommodityRequester:
    @staticmethod
    def retrieve_all_data() -> Union[bool, List[Commodity]]:
        '''Извлечь все модели строк'''
        with db.atomic():
            '''Контекстный менеджер with обеспечит авто-закрытие после запроса.'''
            select_request = Commodity.select()
            if list:
                return list(select_request)
            else:
                return False


    @staticmethod
    def store_data(*data: Union[List[dict], dict], db=db) -> bool:
        '''Загрузка моделей в таблицу товаров'''
        with db.atomic():
            Commodity.insert_many(*data).execute()
            return True



    @staticmethod
    def get_where_state(state: str):
        '''Получение моделей с определённым параметром state(Б/У or NEW)'''
        with db.atomic():
            select_request = Commodity.select().where(Commodity.state == state)
            return list(select_request)


    @staticmethod
    def get_for_request(request: dict):
        '''Вывод моделей подходящих под запрос(используются одни ключи)
        :request[dict]: Желаемый диапазон параметров модели'''
        with db.atomic():
            select_request = Commodity.select().where((Commodity.color == request['color'])
                                                      & (Commodity.commodity_state == request['commodity_state'])
                                                      & (Commodity.car_brand == request['car_brand'])
                                                      & (Commodity.mileage < request['mileage'])
                                                      & (Commodity.model == request['model']))
            return list(select_request)


toyota = {
'brand': 'toyota',
'model': 'supra',
'mileage': 1000000,
'state': 'Б/У',
'color': 'red',
'engine_type': 'america',
'year_of_release': 'america',
'photo_url': 'america',
'complectation': 'america'
}

bmw = {
'brand': 'bmw',
'model': 'x5',
'mileage': 20,
'state': 'новая',
'color': 'black',
'engine_type': 'america',
'year_of_release': 'america',
'photo_url': 'america',
'complectation': 'america'
}

reno = {
'brand': 'renault',
'model': 'logan',
'mileage': 123,
'state': 'новая',
'color': 'pink',
'engine_type': 'america',
'year_of_release': 'america',
'photo_url': 'america',
'complectation': 'america'
}


kamaz = {
'brand': 'kamaz',
'model': 'big',
'mileage': 0,
'state': 'новая',
'color': 'orange',
'engine_type': 'america',
'year_of_release': 'america',
'photo_url': 'america',
'complectation': 'america'
}

new_cars = [kamaz, toyota, bmw, reno]

a = CommodityRequester.store_data(new_cars)