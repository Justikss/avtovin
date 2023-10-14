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
    def get_where_color(color: str):
        '''Получение моделей с определённым параметром color'''
        with db.atomic():
            select_request = Commodity.select().where(Commodity.color == color)
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
