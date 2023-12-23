import importlib
import traceback

from database.data_requests.admin_requests import AdminManager
from database.db_connect import manager
from database.tables.seller import Seller, BannedSeller
from database.tables.user import User, BannedUser
from utils.custom_exceptions.database_exceptions import UserNonExistsError, AdminDoesNotExistsError


class BannedRequester:
    @staticmethod
    async def user_is_blocked(telegram_id, seller=False, user=False):
        if not isinstance(telegram_id, int):
            telegram_id = int(telegram_id)

        if seller:
            ban_table = BannedSeller
        elif user:
            ban_table = BannedUser
        else:
            return False

        banned_user = await manager.get_or_none(ban_table, ban_table.telegram_id == telegram_id)
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
            traceback.print_exc()
            raise UserNonExistsError()

