from database.db_connect import manager
from database.tables.mailing import Mailing


async def create_mailing(recipients_type, text, scheduled_time):
    mailing = await manager.create(Mailing, recipients_type=recipients_type, text=text, scheduled_time=scheduled_time)
    return mailing