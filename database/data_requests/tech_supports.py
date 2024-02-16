from peewee import IntegrityError

from database.db_connect import manager
from database.tables.tech_support_contacts import TechSupports


class TechSupportsManager:
    @staticmethod
    async def get_by_link(link):
        return await manager.get_or_none(TechSupports, link=link)
    @staticmethod
    async def get_by_type(supports_type):
        support_models = list(await manager.execute(TechSupports.select().where(TechSupports.type == supports_type).order_by(TechSupports.id.desc())))
        return support_models

    @staticmethod
    async def get_specific(support_id):
        support_model = await manager.get_or_none(TechSupports, id=support_id)
        return support_model

    @staticmethod
    async def delete(support_id):
        if isinstance(support_id, str):
            support_id = int(support_id)
        try:
            await manager.execute(TechSupports.delete().where(TechSupports.id == support_id))
            return True
        except IntegrityError:
            return False

    @staticmethod
    async def update(support_id, new_link):
        if isinstance(support_id, str):
            support_id = int(support_id)
        if '@' in new_link:
            good_type = 'telegram'
        else:
            good_type = 'number'
        return await manager.execute(TechSupports.update(link=new_link).where(((TechSupports.id == support_id) &
                                                                        (TechSupports.type == good_type))))

    @staticmethod
    async def insert(support_type, link):
        if '@' in link:
            good_type = 'telegram'
        else:
            good_type = 'number'
        if support_type != good_type:
            return False

        return await manager.get_or_create(TechSupports, link=link, type=support_type)