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
    def get_for_request(state: str, brand=None, model=None, engine_type=None,
                        year_of_release=None, complectation=None, mileage=None, color=None):
        '''Вывод моделей подходящих под запрос(используются параметр-ключи)
        :request[dict]: Желаемый диапазон параметров модели'''
        with db.atomic():
            if not brand:
                select_request = Commodity.select().where(Commodity.state == state)
            elif model:
                select_request = Commodity.select().where(Commodity.state == state, Commodity.model == model)
            elif engine_type:
                select_request = Commodity.select().where(Commodity.state == state, Commodity.model == model,
                                                          Commodity.engine_type == engine_type)
            elif complectation:
                select_request = Commodity.select().where(Commodity.state == state, Commodity.model == model,
                                                          Commodity.engine_type == engine_type,
                                                          Commodity.complectation == complectation)
            elif year_of_release:
                select_request = Commodity.select().where(Commodity.state == state, Commodity.model == model,
                                                          Commodity.engine_type == engine_type,
                                                          Commodity.year_of_release == year_of_release)
            elif mileage:
                select_request = Commodity.select().where(Commodity.state == state, Commodity.model == model,
                                                          Commodity.engine_type == engine_type,
                                                          Commodity.year_of_release == year_of_release,
                                                          Commodity.mileage == mileage)
            elif color:
                select_request = Commodity.select().where(Commodity.state == state, Commodity.model == model,
                                                          Commodity.engine_type == engine_type,
                                                          Commodity.year_of_release == year_of_release,
                                                          Commodity.mileage == mileage, Commodity.color == color)
            else:
                select_request = Commodity.select().where(Commodity.state == state, Commodity.brand == brand)

            return list(select_request)



toyota = {
'brand': 'toyota',
'model': 'supra',
'mileage': 1000000,
'state': 'Б/У',
'color': 'red',
'engine_type': 'engine_type-america',
'year_of_release': 'year_of_release-america',
'photo_url': 'america',
'complectation': 'complectation-america',
'price': '750000'
}

bmw = {
'brand': 'bmw',
'model': 'x5',
'mileage': 20,
'state': 'Новая',
'color': 'black',
'engine_type': 'engine_type-lena',
'year_of_release': 'year_of_release-vasya',
'photo_url': 'petya',
'complectation': 'complectation-kolya',
'price': '1500000'
}

reno = {
'brand': 'renault',
'model': 'logan',
'mileage': 123,
'state': 'Новая',
'color': 'pink',
'engine_type': 'engine_type-china',
'year_of_release': 'year_of_release-madrid',
'photo_url': 'africa',
'complectation': 'complectation-uzbekistan',
'price': '300000'
}


kamaz = {
'brand': 'kamaz',
'model': 'big',
'mileage': 0,
'state': 'Новая',
'color': 'orange',
'engine_type': 'engine_type-europa',
'year_of_release': 'year_of_release-america',
'photo_url': 'russia',
'complectation': 'complectation-francia',
'price': '20000000'
}

new_cars = [kamaz, toyota, bmw, reno]

a = CommodityRequester.store_data(new_cars)