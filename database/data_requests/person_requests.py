from typing import Union, List

from peewee import IntegrityError

from database.tables.user import User
from database.tables.start_tables import db
from database.tables.seller import Seller

class PersonRequester:
    @staticmethod
    def retrieve_all_data(user=False, seller=False) -> Union[bool, List[User]]:
        '''Извлечь все модели строк'''
        if user:
            with db.atomic():
                '''Контекстный менеджер with обеспечит авто-закрытие после запроса.'''
                select_request = User.select()
        elif seller:
            with db.atomic():
                '''Контекстный менеджер with обеспечит авто-закрытие после запроса.'''
                select_request = Seller.select()

        if list(select_request):
            return list(select_request)
        else:
            return False


    @staticmethod
    def store_data(*data: Union[List[dict], dict], user=False, seller=False) -> bool:
        '''Загрузка моделей в таблицу товаров'''
        try:
            if user:
                with db.atomic():
                    User.insert_many(*data).execute()
                    return True
            elif seller:
                with db.atomic():
                    Seller.insert_many(*data).execute()
                    return True

        except IntegrityError:
            return False

    @staticmethod
    def get_user_for_id(user_id, user=False, seller=False):
        '''вывод юзера по id юзера в бд'''
        if user:
            with db.atomic():
                print('get_by_user_id', user_id)
                select_request = User.select().where(User.telegram_id == user_id)

        elif seller:
            with db.atomic():
                print('get_by_seller_id', user_id)
                select_request = Seller.select().where(Seller.telegram_id == user_id)

        select_request = list(select_request)
        print(select_request)

        if select_request:
            return select_request
        else:
            return False


seller = [{'telegram_id': '902230076',
'phone_number': '2312342',
'entity': 'fisycal',
'dealship_address': None,
'dealship_name': None,
'name': 'Bo',  # поле ограничено символами(название столбца)
'surname': 'Ri',  # поле ограничено символами(возможно нулевое значение, название столбца)
'patronymic': 'S'},
          ]



PersonRequester.store_data(seller, seller=True)

sellers = PersonRequester.retrieve_all_data(seller=True)


buyer = PersonRequester.retrieve_all_data(user=True)