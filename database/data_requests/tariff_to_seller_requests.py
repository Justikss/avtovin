from typing import Union, List
import datetime

from peewee import DoesNotExist, IntegrityError

from database.data_requests.person_requests import PersonRequester
from database.tables.seller import Seller
from database.tables.tariff import Tariff, TariffsToSellers
from database.data_requests import person_requests, tariff_requests
from utils.custom_exceptions.database_exceptions import NonExistentIdException, NonExistentTariffException, TariffExpiredException, SellerWithoutTariffException
from utils.Lexicon import DateTimeFormat
from config_data.config import DATETIME_FORMAT
from database.db_connect import database, manager



class TariffToSellerBinder:
    @staticmethod
    async def retrieve_all_data() -> Union[bool, List[TariffsToSellers]]:
        '''Асинхронный метод для извлечения всех связей тарифов с продавцами'''
        select_request = await manager.execute(TariffsToSellers.select())
        return list(select_request) if select_request else False

    @staticmethod
    async def get_by_seller_id(seller_id):
        '''Асинхронный метод извлечения модели по телеграм id продавца'''
        query = (TariffsToSellers
                 .select()
                 .join(Seller)
                 .where(Seller.telegram_id == seller_id))
        return await manager.execute(query)

    @staticmethod
    async def feedback_waste(telegram_id):
        '''Асинхронный метод для обработки истраченных отзывов'''
        query = TariffsToSellers.select().where(TariffsToSellers.seller_id == telegram_id)
        total_bind = await manager.execute(query)
        if total_bind:
            total_bind = total_bind[0]
            datetime_now = datetime.datetime.now()
            datetime_tariff_end = total_bind.end_date_time
            if datetime_tariff_end >= datetime_now:
                return query
            else:
                raise TariffExpiredException
        else:
            raise SellerWithoutTariffException

    @staticmethod
    async def set_bind(data: dict) -> bool:
        '''Асинхронный метод установки связей тарифов с продавцом'''
        great_data = await TariffToSellerBinder.__data_extraction_to_boot(data)
        insert_query = TariffsToSellers.insert(**great_data)
        try:
            await manager.execute(insert_query)
        except IntegrityError:
            return False
        return True

    @staticmethod
    async def __data_extraction_to_boot(data):
        '''Асинхронный вспомогательный метод для извлечения и обработки данных'''
        if isinstance(data, dict):
            seller_id = data.get('seller')
            tariff_name = data.get('tariff')
            if seller_id:
                data['seller'] = await PersonRequester.get_user_for_id(user_id=seller_id, seller=True)
                data['seller'] = data['seller'][0] if data['seller'] else None
                if tariff_name:
                    tariff_object = await manager.get(Tariff, Tariff.name == tariff_name)
                    now_time = datetime.datetime.now()
                    end_time = now_time + datetime.timedelta(days=int(tariff_object.duration_time))

                    data['tariff'] = tariff_object
                    data['start_date_time'] = now_time.strftime(DATETIME_FORMAT)
                    data['end_date_time'] = end_time.strftime(DATETIME_FORMAT)
                    data['residual_feedback'] = tariff_object.feedback_amount

                    return data
                else:
                    raise NonExistentTariffException(f'Tariff name {tariff_name} not exist in database.')
            else:
                raise NonExistentIdException(f'Seller id {seller_id} not exist in database.')


    # @classmethod
    # async def set_bind(cls, data: dict) -> bool:
    #     '''Асинхронный метод установки связей тарифов с продавцом'''
    #     great_data = await cls.__data_extraction_to_boot(data)
    #     insert_query = TariffsToSellers.insert(**great_data)
    #     await manager.execute(insert_query)
    #     return True


data = {'seller': '902230076',
'tariff': 'minimum'
}

# TariffToSellerBinder.set_bind(data=data)