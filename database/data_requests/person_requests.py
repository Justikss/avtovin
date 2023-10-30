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

        except IntegrityError as ex:
            print('IntegrityError', ex)
            return False

    @staticmethod
    def this_name_is_exists(name: str, user=None, seller=None):
        '''Проверка на сущестование имени в базе данных'''
        need_model = Seller if seller else User
        
        with db.atomic():
            if seller:
                select_request = list(Seller.select().where(Seller.dealship_name == name))
                if select_request:
                    return True

            
            name = name.split(' ')
            if len(name) == 3:
                patronymic = name[2]
            elif len(name) == 2:
                patronymic = None
            
            surname = name[0]
            name = name[1]

            select_request = list(need_model.select().where((need_model.name == name) &
                                                            (need_model.surname == surname) &
                                                            (need_model.patronymic == patronymic)))
        if select_request:
            return True
        else:
            return False

            

    @staticmethod
    def this_number_is_exists(number: str, user=None, seller=None):
        '''Проверка на существование номера телефона в базе данных'''
        need_model = Seller if seller else User

        with db.atomic():
            select_request = need_model.select().where(need_model.phone_number == number)
            select_request = list(select_request)

        if select_request:
            return True
        else:
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
'entity': 'legal',
'dealship_address': 'Шмеля 15',
'dealship_name': 'MultyReSale',
'name': None,  # поле ограничено символами(название столбца)
'surname': None,  # поле ограничено символами(возможно нулевое значение, название столбца)
'patronymic': None,
'authorized': True}
          ]



#PersonRequester.store_data(seller, seller=True)

sellers = PersonRequester.retrieve_all_data(seller=True)


buyer = PersonRequester.retrieve_all_data(user=True)