from peewee import JOIN

from database.db_connect import manager
from database.tables.mailing import Mailing, ViewedMailing
from database.tables.seller import Seller
from database.tables.user import User
from utils.mailing_heart.mailing_service import mailing_service


async def get_mailings_by_viewed_status(status, get_ids=False):
    mailings = list(await manager.execute(Mailing.select(Mailing).where(Mailing.is_sent == status).order_by(Mailing.id)))
    if get_ids and mailings:
        mailings = [mailing.id for mailing in mailings]
    return mailings

async def create_mailing(text, media, scheduled_time, recipients_type):
    mailing = await manager.create(Mailing, recipients_type=recipients_type, text=text, scheduled_time=scheduled_time,
                                   media=media)
    return mailing

async def get_mailing_by_id(mailing_id):
    if not isinstance(mailing_id, int):
        mailing_id = int(mailing_id)
    return await manager.get_or_none(Mailing, Mailing.id == mailing_id)


async def update_mailing_status(mailing):
    await manager.execute(Mailing.update(is_sent=True).where(Mailing == mailing))

async def view_mailing_action(telegram_ids_to_messages, mailing, user=False, seller=False):
    if isinstance(mailing, Mailing):
        mailing = mailing.id
    elif not isinstance(mailing, int):
        mailing = int(mailing)
    insertable_data = []
    ic(telegram_ids_to_messages, mailing, user, seller)
    for telegram_id, messages in telegram_ids_to_messages.items():
        ic(insertable_data)
        insertable_data.append({
            'message_ids': messages,
            'mailing': mailing,
            'user_id': telegram_id,
            'buyer': user,
            'seller': seller
        })
    if insertable_data:
        ic(insertable_data)
        return await manager.execute(ViewedMailing.insert_many(insertable_data))


async def delete_mailing_action(mailing):
    data_to_delete = None
    if not (isinstance(mailing, int) and not isinstance(mailing, Mailing)):
        mailing = int(mailing)

    viewed_mailings_query = (ViewedMailing
             .select(ViewedMailing)
             .join(Mailing)
             .where(((ViewedMailing.buyer.is_null(False)) | (ViewedMailing.seller.is_null(False))) & (Mailing.id == mailing) & (ViewedMailing.mailing_id == mailing)))

    viewed_mailings = list(await manager.execute(viewed_mailings_query))
    ic(viewed_mailings)
    if viewed_mailings:
        data_to_delete = dict()
        for viewed_mailing in viewed_mailings:
            user_id = viewed_mailing.user_id

            data_to_delete[user_id] = viewed_mailing.message_ids

        ic(data_to_delete)
        if data_to_delete:
            await manager.execute(ViewedMailing.delete().where(ViewedMailing.mailing_id == mailing))
    else:
        await mailing_service.cancel_mailing(mailing)
    await manager.execute(Mailing.delete().where(Mailing.id == mailing))

    if data_to_delete:
        return data_to_delete
