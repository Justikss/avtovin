from database.data_requests.admin_requests import AdminManager
from database.db_connect import manager
from database.tables.seller import Seller
from database.tables.user import User
from utils.custom_exceptions.database_exceptions import UserNonExistsError, AdminDoesNotExistsError


class BannedRequester:
    @staticmethod
    async def set_ban(request, telegram_id, seller=False, user=False):
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
            user_model = await manager.get(current_table, current_table.telegram_id == telegram_id)
            await manager.execute(current_table.delete().where(current_table.telegram_id == telegram_id))
            return user_model
        except:
            raise UserNonExistsError()

