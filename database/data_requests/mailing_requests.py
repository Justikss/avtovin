from database.db_connect import manager
from database.tables.mailing import Mailing


async def create_mailing(text, media, scheduled_time, recipients_type):
    mailing = await manager.create(Mailing, recipients_type=recipients_type, text=text, scheduled_time=scheduled_time,
                                   media=media)
    return mailing

async def retrieve_mailings_that_has_not_been_sent():
    mailings = list(await manager.execute(Mailing.select().where(Mailing.is_sent == False)))
    return mailings

async def update_mailing_status(mailing):
    await manager.execute(Mailing.update(is_sent=True).where(Mailing == mailing))