import importlib
import logging
import traceback
from typing import Union, List

from peewee import IntegrityError, DoesNotExist

from database.data_requests.offers_requests import OffersRequester
from database.data_requests.statistic_requests.advert_feedbacks_requests import AdvertFeedbackRequester
from database.data_requests.tariff_to_seller_requests import TariffToSellerBinder
from database.tables.user import User, BannedUser
from database.db_connect import manager
from database.tables.seller import Seller, BannedSeller
from utils.get_username import get_username

car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')

class PersonRequester:
    @staticmethod
    async def get_all_unique_user_ids():
        sellers = list(await manager.execute(Seller.select(Seller.telegram_id)))
        users = list(await manager.execute(User.select(User.telegram_id)))
        users.extend(sellers)
        result = set()
        for user in users:
            result.add(user.telegram_id)

        return result
    # @staticmethod
    # async def get_by_username(bot, username):
    #     for table in (Seller, User):
    #         user = await manager.get_or_none(table, await get_username(bot, table.telegram_id) == username)
    #         if user:
    #             return user

    @staticmethod
    async def retrieve_all_ids(user=False, seller=False):
        tables = None
        query = None
        current_table = None

        if seller:
            current_table = Seller
        elif user:
            current_table = User
        else:
            tables = [User, Seller]

        if tables:
            queries = []
            for table in tables:
                queries.append(table.select(table.telegram_id))
            query = queries[0] | queries[1]

        elif current_table:
            query = current_table.select(current_table.telegram_id)

        user_ids = list(await manager.execute(query))
        if user_ids:
            user_ids = [user.telegram_id for user in user_ids]

        return user_ids

    @staticmethod
    async def get_by_user_name(name, seller, user, dealership):
        user_model = None
        current_table = None
        name = [name_part.capitalize() for name_part in name.split(' ')]

        ic(name, seller, user, dealership)
        if user:
            current_table = User
        elif seller and not dealership:
            current_table = Seller
        elif seller and dealership:
            user_model = list(await manager.execute(Seller.select().where(Seller.dealship_name == ' '.join(name))))
            current_table = None

        ic(user_model, current_table)
        if not user_model and current_table:
            patronymic = name[2] if len(name) == 3 else None
            surname = name[0]
            name = name[1]
            ic(f'{surname} {name} {patronymic}')
            user_model = list(await manager.execute(current_table.select().where(current_table.name == name,
                                                   current_table.surname == surname,
                                                   current_table.patronymic == patronymic)))
        if len(user_model) == 1:
            user_model = user_model[0]
        ic(user_model)
        return user_model

    @staticmethod
    async def remove_user(telegram_id, seller=False, user=False):
        if not isinstance(telegram_id, int):
            telegram_id = int(telegram_id)
        if seller:
            table_model = Seller
        elif user:
            table_model = User
        else:
            return

        try:
            user_model = await manager.get(table_model, table_model.telegram_id == telegram_id)
            if user_model:
                if user:
                    await OffersRequester.delete_all_buyer_history(telegram_id)
                elif seller:
                    await OffersRequester.delete_seller_offers(telegram_id)
                    await AdvertFeedbackRequester.delete_by_seller_id(telegram_id)

                    await car_advert_requests_module\
                        .AdvertRequester.delete_advert_by_id(telegram_id)
                    await TariffToSellerBinder.remove_bind(telegram_id)
            await manager.execute(table_model.delete().where(table_model.telegram_id == telegram_id))
            return user_model
        except DoesNotExist:
            return False
    @staticmethod
    async def get_seller_by_advert(advert):
        try:
            seller = await manager.get(Seller, Seller.telegram_id == advert.seller)
            return seller
        except:
            pass
            # traceback.print_exc()

    @staticmethod
    async def retrieve_all_data(user=False, seller=False, entity=None) -> Union[bool, List[User]]:
        '''Асинхронный метод для извлечения всех моделей строк'''
        if user:
            return await manager.execute(User.select())
        elif seller:
            if entity:
                query = await manager.execute(Seller.select().where(Seller.entity == entity))
            else:
                query = await manager.execute(Seller.select())
            return list(query)
        else:
            return False

    @staticmethod
    async def store_data(*data: Union[List[dict], dict], user=False, seller=False) -> tuple | bool:
        '''Асинхронный метод для загрузки моделей в таблицу'''
        try:
            current_table = None
            banned_table = None
            ic(data)
            if data:
                user_id = data[0]['telegram_id']

                if user:
                    ic(data)
                    current_table = User
                    banned_table = BannedUser

                elif seller:
                    current_table = Seller
                    banned_table = BannedSeller

                if current_table and banned_table:
                    banned_model = await manager.get_or_none(banned_table, banned_table.telegram_id == user_id)

                    if banned_model:
                        return False
                    else:
                        await manager.execute(current_table.insert_many(*data))
                        return True

        except IntegrityError:
            logging.error('', exc_info=True)
            return False

    @staticmethod
    async def change_authorized_state(telegram_id, boolean: bool):
        '''Асинхронный метод для изменения состояния авторизации продавца'''
        try:
            query = Seller.update(authorized=boolean).where(Seller.telegram_id == telegram_id)
            await manager.execute(query)
            return True
        except IntegrityError:
            logging.error('', exc_info=True)
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
        if  isinstance(user_id, str):
            user_id = int(user_id)

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