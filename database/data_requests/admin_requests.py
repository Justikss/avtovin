import logging

from peewee import IntegrityError, DoesNotExist

from database.db_connect import manager
from database.tables.admin import Admin
from utils.custom_exceptions.database_exceptions import AdminDoesNotExistsError
from utils.get_username import get_username


def to_int(element):
    if isinstance(element, str):
        element = int(element)
    return element

class AdminManager:
    # @staticmethod
    # async def get_admin_by_username(bot, username):
    #     await manager.get_or_none(Admin, await get_username(bot, Admin.telegram_id) == username)
    @staticmethod
    async def set_red_admin(telegram_id):

        admin = await manager.get_or_create(Admin, telegram_id=to_int(telegram_id))
        query = await manager.execute(Admin.update(admin_rang=1).where(Admin.telegram_id == admin[0]))

        return query

    @staticmethod
    async def remove_red_admin(telegram_id):
        try:
            await manager.execute(Admin.update(admin_rang=0).where(Admin.telegram_id == to_int(telegram_id)))
            return True
        except:
            pass

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
        if isinstance(telegram_id, str):
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
        if isinstance(telegram_id, str):
            telegram_id = int(telegram_id)

        delete_query = await manager.execute(Admin.delete().where(Admin.telegram_id == telegram_id))
        if delete_query:
            logging.info(f'Администратор {telegram_id} успешно удалён.')
            return True
        else:
            return False

    @staticmethod
    async def admin_authentication(telegram_id, rang=0):
        if not isinstance(telegram_id, int):
            try:
                telegram_id = int(telegram_id)
            except ValueError:
                return False

        if rang:
            condition = ((Admin.telegram_id == telegram_id) & (Admin.admin_rang == rang))
        else:
            condition = (Admin.telegram_id == telegram_id)

        select_query = Admin.select().where(condition)

        try:
            await manager.get(select_query)
            logging.info(f'Аутентифицирован администратор: {telegram_id}')
            return True
        except DoesNotExist:
            return False
