import importlib
import logging
import traceback

from database.data_requests.admin_requests import AdminManager
from database.db_connect import manager
from database.tables.seller import Seller, BannedSeller
from database.tables.user import User, BannedUser
from utils.custom_exceptions.database_exceptions import UserNonExistsError, AdminDoesNotExistsError

cache_redis_module = importlib.import_module('utils.redis_for_language')
cache_user_status = cache_redis_module.cache_user_status

class BannedRequester:
    @staticmethod
    async def retrieve_all_banned_ids():
        sellers = list(await manager.execute(BannedSeller.select()))
        users = list(await manager.execute(BannedUser.select()))
        users.extend(sellers)
        result = set()
        for user in users:
            result.add(user.telegram_id)

        return result



    @cache_user_status.user_status_cache_decorator(model='ban')
    @staticmethod
    async def user_is_blocked(telegram_id, seller=False, user=False):
        logging.debug('IN USER IS BLOCK CHECK DATABASE METHOD')
        if not isinstance(telegram_id, int):
            telegram_id = int(telegram_id)

        if seller:
            ban_table = BannedSeller
        elif user:
            ban_table = BannedUser
        else:
            return False

        banned_user = await manager.get_or_none(ban_table, ban_table.telegram_id == telegram_id)
        if banned_user:
            banned_user = 'yes'
        else:
            banned_user = 'no'
        ic(banned_user)
        return banned_user

    @staticmethod
    async def check_banned_number(phone_number, seller=False, user=False):
        if seller:
            banned_model = BannedSeller
        elif user:
            banned_model = BannedUser
        else:
            return False
        ic(seller, user)
        banned_model = await manager.get_or_none(banned_model, banned_model.phone_number == phone_number)

        return banned_model

    @cache_user_status.user_status_cache_update_decorator(model='ban')
    @staticmethod
    async def set_ban(request, telegram_id, reason, seller=False, user=False):
        person_requester_module = importlib.import_module('database.data_requests.person_requests')

        try:
            await AdminManager.get_admin(request=request)
        except AdminDoesNotExistsError:
            raise AdminDoesNotExistsError()

        if not isinstance(telegram_id, int):
            telegram_id = int(telegram_id)
        if seller:
            current_table = Seller
            ban_table = BannedSeller
        elif user:
            current_table = User
            ban_table = BannedUser
        else:
            return False

        try:
            ic(current_table, telegram_id)
            user_model = await manager.get(current_table, current_table.telegram_id == telegram_id)
            insert_query = await manager.create(ban_table, telegram_id=telegram_id, phone_number=user_model.phone_number, reason=reason)
            await person_requester_module.PersonRequester.remove_user(telegram_id, seller=seller, user=user)
            ic(insert_query, ban_table, user_model)
            return user_model
        except:
            raise UserNonExistsError()

    @cache_user_status.user_status_cache_update_decorator(model='ban')
    @staticmethod
    async def remove_ban(user_id, seller=False, user=False):
        if isinstance(user_id, str):
            user_id = int(user_id)


        if seller and user:
            for condition in (True, False):
                ic(condition)
                await BannedRequester.remove_ban(user_id, seller=condition, user=not condition)
            return True
        elif seller:
            current_table = BannedSeller
        elif user:
            current_table = BannedUser
        else:
            return
        ic(current_table)
        return await manager.execute(current_table.delete().where(current_table.telegram_id == user_id))

