from typing import Union, List
import datetime

from database.tables.seller import Seller
from database.tables.start_tables import db
from database.tables.tariff import Tariff, TariffsToSellers
from database.data_requests import person_requests, tariff_requests
from utils.custom_exceptions.database_exceptions import NonExistentIdException, NonExistentTariffException
from utils.Lexicon import DateTimeFormat

class TariffToSellerBinder:
    @staticmethod
    def retrieve_all_data() -> Union[bool, List[TariffsToSellers]]:
        '''Извлечь все модели строк'''
        with db.atomic():
            '''Контекстный менеджер with обеспечит авто-закрытие после запроса.'''
            select_request = TariffsToSellers.select()
            print(select_request)
            if list(select_request):
                return list(select_request)
            else:
                return False
    @staticmethod
    def get_by_seller_id(seller_id):
        '''Извлечь модель по телеграм id селлера'''
        with db.atomic():

            query = (TariffsToSellers
            .select()
            .join(Seller)
            .where(Seller.telegram_id == seller_id))

            return list(query)
            # select_response = list(TariffsToSellers.select().where(TariffsToSellers.seller.telegram_id == seller_id))
            # return select_response
            
    @staticmethod
    def feedback_waste(telegram_id):
        with db.atomic():
            total_bind = TariffsToSellers.select().where(TariffsToSellers.seller_id == telegram_id)
            # query = TariffsToSellers.update(residual_feedback=100).where(
            #     TariffsToSellers.seller == telegram_id).execute()
            # return

            if total_bind:
                for model in total_bind:
                    total_feedbacks = model.residual_feedback
                query = TariffsToSellers.update(residual_feedback = total_feedbacks - 1).where(TariffsToSellers.seller == telegram_id).execute()
                return query


    @staticmethod
    def __data_extraction_to_boot(data):
        if isinstance(data, dict):
            seller_id = data.get('seller')
            tariff_name = data.get('tariff')
            if seller_id:
                data['seller'] = person_requests.PersonRequester.get_user_for_id(user_id=seller_id, seller=True)
                data['seller'] = data['seller'][0]
                if tariff_name:
                    tariff_object = Tariff.select().where(Tariff.name == tariff_name)
                    tariff_object = tariff_object[0]
                    now_time = datetime.datetime.now()
                    duration_time = tariff_object.duration_time
                    days = int(duration_time)
                    end_time = now_time + datetime.timedelta(days=days)

                    data['tariff'] = tariff_object
                    data['start_date_time'] = now_time.strftime(DateTimeFormat.get_string)
                    data['end_date_time'] = end_time.strftime(DateTimeFormat.get_string)
                    data['residual_feedback'] = tariff_object.feedback_amount

                    return data

                else:
                    raise NonExistentTariffException(f'Tariff name {tariff_name} not exist in database.')
        else:
            seller_id = data.get('seller')
            raise NonExistentIdException(f'Seller id {seller_id} not exist in database.')


        

    @classmethod
    def set_bind(cls, data: dict, db=db) -> bool:
        '''установка связей тарифов с продавцом'''
        great_data = cls.__data_extraction_to_boot(data=data)

        with db.atomic():    
            model = TariffsToSellers.insert(**great_data).execute()
            return model


data = {'seller': '902230076',
'tariff': 'minimum'
}

# TariffToSellerBinder.set_bind(data=data)