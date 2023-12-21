import logging

from peewee import IntegrityError, DoesNotExist

from database.db_connect import manager
from database.tables.admin import Admin
from utils.custom_exceptions.database_exceptions import AdminDoesNotExistsError


class AdminManager:
    @staticmethod
    async def get_admin(request=None, telegram_id=None):
        if request and not telegram_id:
            telegram_id = request.from_user.id
        elif not isinstance(telegram_id, int):
            telegram_id = int(telegram_id)

        try:
            admin_model = await manager.get(Admin, Admin.telegram_id == telegram_id)
            if not admin_model:
                raise AdminDoesNotExistsError()
            else:
                return admin_model
        except DoesNotExist:
            raise AdminDoesNotExistsError()

    @staticmethod
    async def retrieve_all_admins():
        select_query = Admin.select()
        admins = list(await manager.execute(select_query))
        return admins

    @staticmethod
    async def set_admin(telegram_id):
        if not isinstance(telegram_id, int):
            try:
                telegram_id = int(telegram_id)
            except ValueError:
                return False
        try:
            await manager.create(Admin, telegram_id=telegram_id)
            logging.info(f'Установлен новый администратор: {telegram_id}')
            return True
        except IntegrityError:
            return False

    @staticmethod
    async def remove_admin(telegram_id):
        if not isinstance(telegram_id, int):
            try:
                telegram_id = int(telegram_id)
            except ValueError:
                return False

            delete_query = await manager.execute(Admin.delete().where(Admin.telegram_id == telegram_id))
            if delete_query:
                logging.info(f'Администратор {telegram_id} успешно удалён.')
                return True
            else:
                return False

    @staticmethod
    async def admin_authentication(telegram_id):
        if not isinstance(telegram_id, int):
            try:
                telegram_id = int(telegram_id)
                logging.info(f'Аутентифицирован администратор: {telegram_id}')
            except ValueError:
                return False

        select_query = Admin.select().where(Admin.telegram_id == telegram_id)

        try:
            await manager.get(select_query)
            return True
        except DoesNotExist:
            return False
