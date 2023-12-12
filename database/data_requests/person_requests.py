import traceback
from typing import Union, List

from peewee import IntegrityError

from database.tables.user import User
from database.db_connect import manager
from database.tables.seller import Seller

class PersonRequester:

    @staticmethod
    async def get_seller_by_advert(advert):
        try:
            seller = await manager.get(Seller, Seller.telegram_id == advert.seller)
            return seller
        except:
            traceback.print_exc()

    @staticmethod
    async def retrieve_all_data(user=False, seller=False) -> Union[bool, List[User]]:
        '''Асинхронный метод для извлечения всех моделей строк'''
        if user:
            return await manager.execute(User.select())
        elif seller:
            return await manager.execute(Seller.select())
        else:
            return False

    @staticmethod
    async def store_data(*data: Union[List[dict], dict], user=False, seller=False) -> tuple | bool:
        '''Асинхронный метод для загрузки моделей в таблицу'''
        try:
            if user:
                ic(data)
                await manager.execute(User.insert_many(*data))
                return True
            elif seller:
                await manager.execute(Seller.insert_many(*data))
                return True
        except IntegrityError as ex:
            print('IntegrityError', ex)
            return False, ex

    @staticmethod
    async def change_authorized_state(telegram_id, boolean: bool):
        '''Асинхронный метод для изменения состояния авторизации продавца'''
        try:
            query = Seller.update(authorized=boolean).where(Seller.telegram_id == telegram_id)
            await manager.execute(query)
            return True
        except IntegrityError as ex:
            print(ex)
            return False

    @staticmethod
    async def this_name_is_exists(name: str, user=None, seller=None):
        '''Асинхронная проверка на существование имени в базе данных'''
        need_model = Seller if seller else User
        query = need_model.select().where(need_model.name == name)
        result = await manager.execute(query)
        return bool(result)


    @staticmethod
    async def this_number_is_exists(number: str, user=None, seller=None):
        '''Асинхронная проверка на существование номера телефона в базе данных'''
        need_model = Seller if seller else User
        query = need_model.select().where(need_model.phone_number == number)
        result = await manager.execute(query)
        return bool(result)

    @staticmethod
    async def get_user_for_id(user_id, user=False, seller=False):
        '''Асинхронный вывод пользователя по id в бд'''
        if user:
            query = User.select().where(User.telegram_id == user_id)
        elif seller:
            query = Seller.select().where(Seller.telegram_id == user_id)
        result = await manager.execute(query)
        return list(result) if result else False


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

# sellers = PersonRequester.retrieve_all_data(seller=True)


# buyer = PersonRequester.retrieve_all_data(user=True)