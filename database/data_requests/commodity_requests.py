from typing import Union, List

from peewee import IntegrityError

from database.tables.commodity import Commodity
from database.tables.start_tables import db
from database.data_requests.person_requests import sellers, buyer
import sqlite3

class CommodityRequester:
    @staticmethod
    def retrieve_all_data() -> Union[bool, List[Commodity]]:
        '''Извлечь все модели строк'''
        with db.atomic():
            '''Контекстный менеджер with обеспечит авто-закрытие после запроса.'''
            select_request = Commodity.select()
            print(select_request)
            if list(select_request):
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
    def get_car_for_offer(seller_id: int, car_range_id: list):
        '''Получение моделей с определённым параметром state(Б/У or NEW)'''
        with db.atomic():
            models = list()
            for car_id in car_range_id:
                models.append(Commodity.get_by_id(car_id))
                print('pre-yes', models)
            if models:
                print(type(models[0].seller_id), models[0].seller_id)
                models = [model for model in models if model.seller_id.telegram_id == seller_id]
                print('pre-yes', models, type(seller_id), seller_id)

                if models:
                    print('yes', models)
                    return models

            return False

            #
            #
            # result = list()
            # for current_car_id in car_range_id:
            #     print(current_car_id)
            #     select_request = Commodity.select().where(
            #                                     (Commodity.seller_id == seller_id) &
            #                                     (Commodity.car_id == current_car_id)
            #             )
            #         # .order_by(-Commodity.id)  # Сортировка по убыванию ID для обратного порядка
            #     print(select_request)
            #     if list(select_request):
            #         result.append(list(select_request)[0])
            # if result:
            #     return result
            # else:
            #     return False
        # print('res', list(select_request))
        # return list(select_request)



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
        print('infa', state, brand, model, engine_type, year_of_release, complectation, mileage, color)
        with db.atomic():
            if not brand:
                print('yes not brand')
                select_request = Commodity.select().where(Commodity.state == state)

            elif brand and not model:
                print('yes brand')
                select_request = Commodity.select().where((Commodity.state == state) &
                                                          (Commodity.brand == brand))

            elif model and not engine_type:
                print('yes model')
                select_request = Commodity.select().where((Commodity.state == state) &
                                                          (Commodity.brand == brand) &
                                                          (Commodity.model == model))

            elif engine_type and not complectation or year_of_release:
                print('yes engine')
                select_request = Commodity.select().where((Commodity.state == state) &
                                 (Commodity.brand == brand) &
                                 (Commodity.model == model) &
                                 (Commodity.engine_type == engine_type))

            elif complectation:

                print('yes_complectation')
                select_request = Commodity.select().where((Commodity.state == state) &
                                 (Commodity.brand == brand) &
                                 (Commodity.model == model) &
                                 (Commodity.engine_type == engine_type) &
                                 (Commodity.complectation == complectation))
            elif year_of_release and not mileage:
                print('yes year realise')
                select_request = Commodity.select().where((Commodity.state == state) &
                                 (Commodity.brand == brand) &
                                 (Commodity.model == model) &
                                 (Commodity.engine_type == engine_type) &
                                 (Commodity.year_of_release == year_of_release))
            elif mileage and not color:
                print('yes mileage')
                select_request = Commodity.select().where((Commodity.state == state) &
                                 (Commodity.brand == brand) &
                                 (Commodity.model == model) &
                                 (Commodity.engine_type == engine_type) &
                                 (Commodity.year_of_release == year_of_release) &
                                 (Commodity.mileage == mileage))
            elif color:
                print('yes color')
                select_request = Commodity.select().where((Commodity.state == state) &
                                 (Commodity.brand == brand) &
                                 (Commodity.model == model) &
                                 (Commodity.engine_type == engine_type) &
                                 (Commodity.year_of_release == year_of_release) &
                                 (Commodity.mileage == mileage) &
                                 (Commodity.color == color))
            else:
                print('yes no')
                select_request = Commodity.select().where((Commodity.state == state) &
                                 (Commodity.brand == brand))
            print([comm.model for comm in list(select_request)])
            return list(select_request)

bmwA = {
'seller_id': sellers[0],
'brand': 'bmw',
'model': 'x6',
'mileage': '1000000',
'state': 'Б/У',
'color': 'white',
'engine_type': 'DWS',
'year_of_release': '23',
'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fnetcarflix.sfo2.cdn.digitaloceanspaces.com%2F0000%2Fv3%2FBMW%2F64366b3d31a7f6873c2f1ed0%2F2020-x6-bmw-3jrus3llln10rxvy5no88s.jpeg&lr=172&pos=0&rpt=simage&text=bmw%20x6',
'complectation': None,
'price': '750000'
}

bmww = {
'seller_id': sellers[0],
'brand': 'bmw',
'model': 'm5',
'mileage': '1000000',
'state': 'Б/У',
'color': 'red',
'engine_type': 'DWS',
'year_of_release': '21',
'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fwallpapershome.com%2Fimages%2Fwallpapers%2Fbmw-m5-5120x2880-cars-2018-5k-17134.jpg&lr=172&noreask=1&pos=0&rpt=simage&text=BMW%20M5',
'complectation': None,
'price': '750000'
}

ebw = {
'seller_id': sellers[0],
'brand': 'bmw',
'model': 'm8',
'mileage': '1000000',
'state': 'Б/У',
'color': 'red',
'engine_type': 'Hybrid',
'year_of_release': '21',
'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fhips.hearstapps.com%2Fhmg-prod%2Fimages%2F2020-bmw-m8-coupe-105-1559695155.jpg%3Fcrop%3D1.00xw%3A0.753xh%3B0%2C0.247xh%26amp%3Bresize%3D640%3A*&lr=172&pos=0&rpt=simage&text=BMW%20M8',
'complectation': None,
'price': '7000'
}

bmw = {
'seller_id': sellers[0],
'brand': 'bmw',
'model': 'x5',
'engine_type': 'DWS',
'state': 'Новая',
'color': None,
'mileage': None,
'year_of_release': None,
'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fbipbap.ru%2Fwp-content%2Fuploads%2F2018%2F08%2Fhamman-bmw-x5-1.jpg&lr=172&pos=0&rpt=simage&text=bmw%20x5',
'complectation': 'complectation7',
'price': '1000000'
}

bmwww = {
'seller_id': sellers[0],
'brand': 'bmw',
'model': 'e34',
'engine_type': 'DWS',
'state': 'Новая',
'color': None,
'mileage': None,
'year_of_release': None,
'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fa.d-cd.net%2Fa4f42es-1920.jpg&lr=172&pos=0&rpt=simage&text=BMW%20e34',
'complectation': 'complectation2',
'price': '1500000'
}


mbw = {
'seller_id': sellers[0],
'brand': 'bmw',
'model': 'e34',
'engine_type': 'Hybrid',
'state': 'Новая',
'color': None,
'mileage': None,
'year_of_release': None,
'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fimg1.goodfon.ru%2Foriginal%2F2000x1333%2F3%2F2d%2Fbmw-e34-stance-bbs.jpg&lr=172&pos=8&rpt=simage&text=BMW%20e34',
'complectation': 'complectation3',
'price': '2000000'
}

www = {
'seller_id': sellers[0],
'brand': 'bmw',
'model': 'e34',
'engine_type': 'DWS',
'state': 'Новая',
'color': None,
'mileage': None,
'year_of_release': None,
'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fsun9-39.userapi.com%2Fimpg%2F4RKwjC-Bqw_4qYk_yet0wkebDRKF-l29yGnGbA%2FuKCqfz0g8Ko.jpg%3Fsize%3D1280x853%26quality%3D96%26sign%3D288da2c93ca8f1ebd7b0bf11fb39825d%26c_uniq_tag%3D2bNkumiVDgQ36iCCoBJOHqFr6yhtVLrcLER_sYR15Jo%26type%3Dalbum&lr=172&pos=24&rpt=simage&text=BMW%20e34',
'complectation': 'complectation1',
'price': '3000000'
}


new_cars = [bmww, ebw, bmw, bmwww, mbw, www, bmwA]

double_cars = www = {
'seller_id': sellers[0],
'brand': 'bmw',
'model': 'e34',
'engine_type': 'DWS',
'state': 'Новая',
'color': None,
'mileage': None,
'year_of_release': None,
'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fsun9-39.userapi.com%2Fimpg%2F4RKwjC-Bqw_4qYk_yet0wkebDRKF-l29yGnGbA%2FuKCqfz0g8Ko.jpg%3Fsize%3D1280x853%26quality%3D96%26sign%3D288da2c93ca8f1ebd7b0bf11fb39825d%26c_uniq_tag%3D2bNkumiVDgQ36iCCoBJOHqFr6yhtVLrcLER_sYR15Jo%26type%3Dalbum&lr=172&pos=24&rpt=simage&text=BMW%20e34',
'complectation': 'complectation1',
'price': '200'
}
#a = CommodityRequester.store_data(double_cars)


cars = CommodityRequester.retrieve_all_data()
