from typing import Union, List

from peewee import IntegrityError

from database.tables.commodity import AdvertPhotos

from database.tables.car_configurations import CarAdvert
from database.tables.offers_history import ActiveOffers, CacheBuyerOffers

# from database.data_requests.person_requests import sellers, buyer


class CommodityRequester:
    @staticmethod
    def delete_car_by_id(car_id):
        '''Удаление автомобиля'''
        with db.atomic():
            select_response = CarAdvert.delete_by_id(car_id)
            if select_response:
                select_response_offers_history = ActiveOffers.delete().where(ActiveOffers.car_id == car_id).execute()
                ic(select_response_offers_history)

                response_delete_user_cache_with_car = CacheBuyerOffers.delete().where(CacheBuyerOffers.car_id == car_id).execute()
                ic(response_delete_user_cache_with_car)
                select_response_photography = CommodityPhotos.delete().where(CommodityPhotos.car_id == car_id).execute()
                print('selectete: ', select_response_photography)
                if select_response_photography:
                    return select_response

            return False



    @staticmethod
    def retrieve_all_data() -> Union[bool, List[CarAdvert]]:
        '''Извлечь все модели строк'''
        with db.atomic():
            '''Контекстный менеджер with обеспечит авто-закрытие после запроса.'''
            select_request = CarAdvert.select()
            print(select_request)
            if list(select_request):
                return list(select_request)
            else:
                return False

    @staticmethod
    def store_data(data: Union[List[dict], dict], db) -> bool:
        '''Загрузка моделей в таблицу товаров'''
        if isinstance(data, dict):
            data = [data]  # Убедитесь, что данные всегда в виде списка

        with db.atomic():
            photo_boot_data = []

            for data_part in data:
                photo_data = data_part.pop('photos')
                # Вставка каждой записи в CarAdvert отдельно
                CarAdvert_model = CarAdvert.insert(**data_part).execute()

                if photo_data:
                    if isinstance(photo_data, list):
                        for photo_data_part in photo_data:
                            photo_boot_data.append({
                            'car_id': CarAdvert_model,  # Использование идентификатора вставленной записи
                            'photo_id': photo_data_part['id'],
                            'photo_unique_id': photo_data_part['unique_id']
                        })
                    else:
                        ic(photo_data)
                        if len(photo_data) == 1:
                            photo_data = [photo_part for photo_part in photo_data.values()]

                        if len(photo_data) == 1:
                            photo_data = photo_data[0]
                        ic(photo_data)
                        ic(len(photo_data))
                        for photo_data_part in photo_data:
                            if isinstance(photo_data_part, list):
                                photo_data_part = photo_data_part[0]
                            print('iteration')
                            ic(photo_data_part)
                            photo_boot_data.append({
                                'car_id': CarAdvert_model,  # Использование идентификатора вставленной записи
                                'photo_id': photo_data_part['id'],
                                'photo_unique_id': photo_data_part['unique_id']
                            })

            if photo_boot_data:
                ic(photo_boot_data)
                CommodityPhotos.insert_many(photo_boot_data).execute()

            return CarAdvert_model


    @staticmethod
    def get_where_state(state: str):
        '''Получение моделей с определённым параметром state(Б/У or NEW)'''
        with db.atomic():
            select_request = CarAdvert.select().where(CarAdvert.state == state)
            return list(select_request)

    @staticmethod
    def get_car_for_offer(seller_id: int, car_range_id: list):
        '''Получение моделей с определённым параметром state(Б/У or NEW)'''
        with db.atomic():
            models = list()
            for car_id in car_range_id:
                models.append(CarAdvert.get_by_id(car_id))
                print('pre-yes', models)
            if models:
                models = [model for model in models if model.seller_id.telegram_id == seller_id]
                print('pre-yes', models, type(seller_id), seller_id)

                if models:
                    print('yes', models)
                    return models

            return False


    @staticmethod
    def get_by_seller_id(seller_id):
        '''Получить автомобили по id продавца'''
        with db.atomic():
            sellers_commodities = list(CarAdvert.select().where(CarAdvert.seller_id == seller_id))
            print('commodities_db ', sellers_commodities)
            if sellers_commodities:
                return sellers_commodities
            else:
                return False

    @staticmethod
    def get_by_seller_id_and_brand(seller_id, car_brand):
        '''Получить автомобили по id продавца и марке машины'''
        with db.atomic():
            print(seller_id, car_brand)
            sellers_commodities = list(CarAdvert.select().where((CarAdvert.seller_id == seller_id) &
                                                                (CarAdvert.brand == car_brand)))
            if sellers_commodities:
                return sellers_commodities
            else:
                return False



    @staticmethod
    def get_for_request(state: str, brand=None, model=None, engine_type=None,
                        year_of_release=None, complectation=None, mileage=None, color=None):
        '''Вывод моделей подходящих под запрос(используются параметр-ключи)
        :request[dict]: Желаемый диапазон параметров модели'''
        print('infa', state, brand, model, engine_type, year_of_release, complectation, mileage, color)
        with db.atomic():
            if not engine_type:
                print('yes not engine_type')
                select_request = CarAdvert.select().where(CarAdvert.state == state)

            elif engine_type and not brand:
                print('yes brand')
                select_request = CarAdvert.select().where((CarAdvert.state == state) &
                                                          (CarAdvert.engine_type == engine_type))

            elif brand and not model:
                print('yes model')
                select_request = CarAdvert.select().where((CarAdvert.state == state) &
                                                          (CarAdvert.brand == brand) &
                                                          (CarAdvert.engine_type == engine_type))

            elif model and not complectation:
                print('yes engine')
                select_request = CarAdvert.select().where((CarAdvert.state == state) &
                                 (CarAdvert.brand == brand) &
                                 (CarAdvert.model == model) &
                                 (CarAdvert.engine_type == engine_type))

            elif complectation and not color:

                print('yes_complectation')
                select_request = CarAdvert.select().where((CarAdvert.state == state) &
                                 (CarAdvert.brand == brand) &
                                 (CarAdvert.model == model) &
                                 (CarAdvert.engine_type == engine_type) &
                                 (CarAdvert.complectation == complectation))

            elif color and not mileage:
                print('yes year realise')
                select_request = CarAdvert.select().where((CarAdvert.state == state) &
                                 (CarAdvert.brand == brand) &
                                 (CarAdvert.model == model) &
                                 (CarAdvert.engine_type == engine_type) &
                                 (CarAdvert.color == color))

            elif mileage and not year_of_release:
                print('yes mileage')
                select_request = CarAdvert.select().where((CarAdvert.state == state) &
                                 (CarAdvert.brand == brand) &
                                 (CarAdvert.model == model) &
                                 (CarAdvert.engine_type == engine_type) &
                                 (CarAdvert.color == color) &
                                 (CarAdvert.mileage == mileage))
            elif year_of_release:
                print('yes color')
                select_request = CarAdvert.select().where((CarAdvert.state == state) &
                                 (CarAdvert.brand == brand) &
                                 (CarAdvert.model == model) &
                                 (CarAdvert.engine_type == engine_type) &
                                 (CarAdvert.year_of_release == year_of_release) &
                                 (CarAdvert.mileage == mileage) &
                                 (CarAdvert.color == color))
            else:
                print('COMMMODITY REQUEEEEST ELSEEEEEEEEEE')
            print([comm.model for comm in list(select_request)])
            return list(select_request)

# bmwA = {
# 'seller_id': sellers[0],
# 'brand': 'bmw',
# 'model': 'x6',
# 'mileage': '1000000',
# 'state': 'Б/У',
# 'color': 'white',
# 'engine_type': 'DWS',
# 'year_of_release': '23',
# 'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fnetcarflix.sfo2.cdn.digitaloceanspaces.com%2F0000%2Fv3%2FBMW%2F64366b3d31a7f6873c2f1ed0%2F2020-x6-bmw-3jrus3llln10rxvy5no88s.jpeg&lr=172&pos=0&rpt=simage&text=bmw%20x6',
# 'complectation': 'complectation2',
# 'price': '750000'
# }

# bmww = {
# 'seller_id': sellers[0],
# 'brand': 'bmw',
# 'model': 'm5',
# 'mileage': '1000000',
# 'state': 'Б/У',
# 'color': 'red',
# 'engine_type': 'DWS',
# 'year_of_release': '21',
# 'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fwallpapershome.com%2Fimages%2Fwallpapers%2Fbmw-m5-5120x2880-cars-2018-5k-17134.jpg&lr=172&noreask=1&pos=0&rpt=simage&text=BMW%20M5',
# 'complectation': 'complectation7',
# 'price': '750000'
# }

# ebw = {
# 'seller_id': sellers[0],
# 'brand': 'bmw',
# 'model': 'm8',
# 'mileage': '1000000',
# 'state': 'Б/У',
# 'color': 'red',
# 'engine_type': 'Hybrid',
# 'year_of_release': '21',
# 'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fhips.hearstapps.com%2Fhmg-prod%2Fimages%2F2020-bmw-m8-coupe-105-1559695155.jpg%3Fcrop%3D1.00xw%3A0.753xh%3B0%2C0.247xh%26amp%3Bresize%3D640%3A*&lr=172&pos=0&rpt=simage&text=BMW%20M8',
# 'complectation': 'complectation7',
# 'price': '7000'
# }

# bmw = {
# 'seller_id': sellers[0],
# 'brand': 'bmw',
# 'model': 'x5',
# 'engine_type': 'DWS',
# 'state': 'Новая',
# 'color': None,
# 'mileage': None,
# 'year_of_release': None,
# 'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fbipbap.ru%2Fwp-content%2Fuploads%2F2018%2F08%2Fhamman-bmw-x5-1.jpg&lr=172&pos=0&rpt=simage&text=bmw%20x5',
# 'complectation': 'complectation7',
# 'price': '1000000'
# }

# bmwww = {
# 'seller_id': sellers[0],
# 'brand': 'bmw',
# 'model': 'e34',
# 'engine_type': 'DWS',
# 'state': 'Новая',
# 'color': None,
# 'mileage': None,
# 'year_of_release': None,
# 'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fa.d-cd.net%2Fa4f42es-1920.jpg&lr=172&pos=0&rpt=simage&text=BMW%20e34',
# 'complectation': 'complectation2',
# 'price': '1500000'
# }


# mbw = {
# 'seller_id': sellers[0],
# 'brand': 'bmw',
# 'model': 'e34',
# 'engine_type': 'Hybrid',
# 'state': 'Новая',
# 'color': None,
# 'mileage': None,
# 'year_of_release': None,
# 'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fimg1.goodfon.ru%2Foriginal%2F2000x1333%2F3%2F2d%2Fbmw-e34-stance-bbs.jpg&lr=172&pos=8&rpt=simage&text=BMW%20e34',
# 'complectation': 'complectation3',
# 'price': '2000000'
# }

# www = {
# 'seller_id': sellers[0],
# 'brand': 'bmw',
# 'model': 'e34',
# 'engine_type': 'DWS',
# 'state': 'Новая',
# 'color': None,
# 'mileage': None,
# 'year_of_release': None,
# 'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fsun9-39.userapi.com%2Fimpg%2F4RKwjC-Bqw_4qYk_yet0wkebDRKF-l29yGnGbA%2FuKCqfz0g8Ko.jpg%3Fsize%3D1280x853%26quality%3D96%26sign%3D288da2c93ca8f1ebd7b0bf11fb39825d%26c_uniq_tag%3D2bNkumiVDgQ36iCCoBJOHqFr6yhtVLrcLER_sYR15Jo%26type%3Dalbum&lr=172&pos=24&rpt=simage&text=BMW%20e34',
# 'complectation': 'complectation1',
# 'price': '3000000'
# }


# new_cars = [bmww, ebw, bmw, bmwww, mbw, www, bmwA]

# double_cars = {
# 'seller_id': sellers[0],
# 'brand': 'bmw',
# 'model': 'e34',
# 'engine_type': 'DWS',
# 'state': 'Новая',
# 'color': None,
# 'mileage': None,
# 'year_of_release': None,
# 'photo_url': 'https://yandex.ru/images/search?from=tabbar&img_url=https%3A%2F%2Fsun9-39.userapi.com%2Fimpg%2F4RKwjC-Bqw_4qYk_yet0wkebDRKF-l29yGnGbA%2FuKCqfz0g8Ko.jpg%3Fsize%3D1280x853%26quality%3D96%26sign%3D288da2c93ca8f1ebd7b0bf11fb39825d%26c_uniq_tag%3D2bNkumiVDgQ36iCCoBJOHqFr6yhtVLrcLER_sYR15Jo%26type%3Dalbum&lr=172&pos=24&rpt=simage&text=BMW%20e34',
# 'complectation': 'complectation1',
# 'price': '200'
# }

truple_car = []
truple_car.append({
    'seller_id': 902230076,
    'brand': 'BMW',
    'model': 'OneModel',
    'engine_type': 'DWS',
    'state': 'Новое',
    'color': None,
    'mileage': None,
    'year_of_release': None,
    'complectation': 'FullComplectation',
    'price': '200000',
    'photos': None
})

truple_car.append({
    'seller_id': 902230076,
    'brand': 'Renault',
    'model': 'OneModel',
    'engine_type': 'DWS',
    'state': 'Новое',
    'color': None,
    'mileage': None,
    'year_of_release': None,
    'complectation': 'FullComplectation',
    'price': '200000',
    'photos': None
})



truple_car.append({
    'seller_id': 902230076,
    'brand': 'Skoda',
    'model': 'OneModel',
    'engine_type': 'DWS',
    'state': 'Новое',
    'color': None,
    'mileage': None,
    'year_of_release': None,
    'complectation': 'FullComplectation',
    'price': '200000',
    'photos': None
})



# a = CarAdvertRequester.store_data(double_cars)
#b = CarAdvertRequester.store_data(new_cars)
# c = CarAdvertRequester.store_data(truple_car)


# cars = CarAdvertRequester.retrieve_all_data()
