from typing import Union, List

from database.tables.user import User
from database.tables.start_tables import db

class UserRequester:
    @staticmethod
    def retrieve_all_data() -> Union[bool, List[User]]:
        '''Извлечь все модели строк'''
        with db.atomic():
            '''Контекстный менеджер with обеспечит авто-закрытие после запроса.'''
            select_request = User.select()
            if list(select_request):
                return list(select_request)
            else:
                return False


    @staticmethod
    def store_data(*data: Union[List[dict], dict]) -> bool:
        '''Загрузка моделей в таблицу товаров'''
        with db.atomic():
            User.insert_many(*data).execute()
            return True

    @staticmethod
    def get_user_for_id(user_id):
        '''вывод юзера по id юзера в бд'''
        with db.atomic():
            select_request = User.select().where(User.telegram_id == user_id)
            select_request = list(select_request)
            if select_request:
                return select_request
            else:
                return False

