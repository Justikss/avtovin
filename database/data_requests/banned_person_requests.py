import datetime
import importlib
import logging
import traceback

from database.data_requests.admin_requests import AdminManager
from database.db_connect import manager
from database.tables.seller import Seller
from database.tables.user import User
from utils.custom_exceptions.database_exceptions import UserNonExistsError, AdminDoesNotExistsError

cache_redis_module = importlib.import_module('utils.redis_for_language')
cache_user_status = cache_redis_module.cache_user_status

def block_status_condition(table, condition = None, block_mode='false'):
    ic(block_mode)
    match block_mode:
        case 'true':
            ban_condition = table.is_banned == True
        case 'false':
            ban_condition = table.is_banned == False
        case _:
            raise ValueError('User block status non implemented')
            # ban_condition = table.is_banned == False

    if condition:
        condition = ((ban_condition) & (condition))
    else:
        condition = ban_condition
    return condition
class BannedRequester:
    @staticmethod
    async def retrieve_banned_users(seller=False, user=False, entity=None):
        if seller:
            table = Seller
        elif user:
            table = User
        else:
            return

        if seller and entity:
            query = Seller.select().where(block_status_condition(Seller, Seller.entity == entity, 'true'))
        else:
            query = table.select().where(block_status_condition(table, block_mode='true'))

        result = list(await manager.execute(query))
        ic(result)
        return result


    @staticmethod
    async def retrieve_all_banned_ids():
        all_users = []
        tables = (Seller, User)
        for table in tables:
            users = list(await manager.execute(table.select(table.telegram_id)
                                               .where(block_status_condition(table, block_mode='true'))))
            all_users.extend(users)

        result = set()
        for user in all_users:
            result.add(user.telegram_id)

        all_users = list(all_users)

        return all_users



    @cache_user_status.user_status_cache_decorator(model='ban')
    @staticmethod
    async def user_is_blocked(telegram_id, seller=False, user=False):
        logging.debug('IN USER IS BLOCK CHECK DATABASE METHOD')
        banned_user = 'no'
        if not isinstance(telegram_id, int):
            telegram_id = int(telegram_id)

        if seller:
            ban_table = Seller
        elif user:
            ban_table = User
        else:
            return False

        user = await manager.get_or_none(ban_table, ban_table.telegram_id == telegram_id)

        if user:
            if user.is_banned:
                banned_user = 'yes'
        ic(banned_user, telegram_id)
        # if not banned_user:
        #     banned_user = 'no'
        # ic(banned_user, user.__dict__)
        return banned_user

    @staticmethod
    async def check_banned_number(phone_number, seller=False, user=False):
        if seller:
            banned_model = Seller
        elif user:
            banned_model = User
        else:
            return False
        ic(seller, user)
        banned_model = await manager.get_or_none(banned_model, block_status_condition(
            banned_model,
            banned_model.phone_number == phone_number, 'true'))

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
        elif user:
            current_table = User
        else:
            return False

        try:
            ic(current_table, telegram_id)
            user_model = await manager.get(current_table, current_table.telegram_id == telegram_id)

            update_query = (current_table.update(is_banned=True, ban_reason=reason, block_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
                            .where(current_table.telegram_id == telegram_id))
            await manager.execute(update_query)
            from database.data_requests.person_requests import PersonRequester
            await PersonRequester.remove_user_history(telegram_id, seller=seller, user=user)
            return user_model
        except:
            traceback.print_exc()
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
            current_table = Seller
        elif user:
            current_table = User
        else:
            return
        ic(current_table)
        update_query = (current_table.update(is_banned=False, ban_reason=None, block_date=None)
                        .where(current_table.telegram_id == user_id))
        result = await manager.execute(update_query)
        return result

