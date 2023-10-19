from typing import Union, List

from peewee import IntegrityError

from database.tables.commodity import Commodity
from database.tables.start_tables import db
from database.data_requests.person_requests import sellers, buyer

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
    def get_car_for_offer(seller_id: int, car_range_id: tuple):
        '''Получение моделей с определённым параметром state(Б/У or NEW)'''
        with db.atomic():
            select_request = Commodity.select().where(Commodity.seller_id == seller_id, Commodity.car_id in car_range_id)
            return list(select_request)

    @staticmethod
    def get_where_id(car_id: str):
        '''Получение моделей с определённым параметром id'''
        try:
            with db.atomic():
                select_request = Commodity.select().where(Commodity.car_id == int(car_id))
                return list(select_request)
        except Exception:
            return False

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
'seller_id': sellers[0],
'brand': 'toyota',
'model': 'supra',
'mileage': '1000000',
'state': 'Б/У',
'color': 'red',
'engine_type': 'engine_type-america',
'year_of_release': 'year_of_release-america',
'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Ftopworldauto.com%2Fphotos%2Fcd%2F03%2F2013-toyota-corolla-sport-car_b4380.jpg&lr=172&pos=2&rpt=simage&text=toyota',
'complectation': 'complectation-america',
'price': '750000'
}

bmw = {
'seller_id': sellers[0],
'brand': 'bmw',
'model': 'x5',
'mileage': '20',
'state': 'Новая',
'color': 'black',
'engine_type': 'engine_type-lena',
'year_of_release': 'year_of_release-vasya',
'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fbipbap.ru%2Fwp-content%2Fuploads%2F2018%2F08%2Fhamman-bmw-x5-1.jpg&lr=172&pos=0&rpt=simage&text=bmw%20x5',
'complectation': 'complectation-kolya',
'price': '1500000'
}

reno = {
'seller_id': sellers[0],
'brand': 'renault',
'model': 'logan',
'mileage': '123',
'state': 'Новая',
'color': 'pink',
'engine_type': 'engine_type-china',
'year_of_release': 'year_of_release-madrid',
'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fcarsweek.ru%2Fupload%2F2021%2F%25D0%259E%25D0%25BA%25D1%2582%25D1%258F%25D0%25B1%25D1%2580%25D1%258C%2F10%2F2.jpg&lr=172&pos=0&rpt=simage&text=reno',
'complectation': 'complectation-uzbekistan',
'price': '300000'
}


kamaz = {
'seller_id': sellers[0],
'brand': 'kamaz',
'model': 'big',
'mileage': '0',
'state': 'Новая',
'color': 'orange',
'engine_type': 'engine_type-europa',
'year_of_release': 'year_of_release-america',
'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fautobagi.lt%2Fimages%2FKamaz%2Fsavivarciai%2F65115%2F3.jpg&lr=172&pos=2&rpt=simage&text=kamaz',
'complectation': 'complectation-francia',
'price': '20000000'
}

# new_cars = [kamaz, toyota, bmw, reno]
#
# a = CommodityRequester.store_data(new_cars)


cars = CommodityRequester.retrieve_all_data()
