from peewee import JOIN

from database.db_connect import manager
from database.tables.mailing import Mailing, ViewedMailing
from database.tables.seller import Seller
from database.tables.user import User


async def get_mailings_by_viewed_status(status, get_ids=False):
    mailings = list(await manager.execute(Mailing.select(Mailing.id).where(Mailing.is_sent == status)))
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

async def retrieve_mailings_that_has_not_been_sent():
    mailings = list(await manager.execute(Mailing.select().where(Mailing.is_sent == False)))
    return mailings

async def update_mailing_status(mailing):
    await manager.execute(Mailing.update(is_sent=True).where(Mailing == mailing))

async def view_action(telegram_ids_to_messages, mailing, user=None, seller=None):
    if user or seller:
        insertable_data = []
        for telegram_id, messages in telegram_ids_to_messages.items():
            if user:
                user = telegram_id
            elif seller:
                seller = telegram_id
            insertable_data.append({
                'message_ids': messages,
                'mailing': mailing,
                'buyer': user,
                'seller': seller
            })
        if insertable_data:
            return await manager.execute(ViewedMailing.insert_many(*insertable_data))


async def delete_viewed_mailing_action(mailing):
    # mailing = list(await manager.execute(Mailing.select(Mailing, ViewedMailing).join(ViewedMailing).where(
    #     (Mailing.is_sent == True) & (Mailing == mailing) & (ViewedMailing.mailing_id == mailing.id)
    # )))
    if not (isinstance(mailing, int) or isinstance(mailing, Mailing)):
        mailing = int(mailing)

    viewed_mailings_query = (ViewedMailing
             .select(ViewedMailing, User, Seller)
             .join(User, JOIN.LEFT_OUTER, on=(ViewedMailing.buyer == User.telegram_id))
             .switch(ViewedMailing)
             .join(Seller, JOIN.LEFT_OUTER, on=(ViewedMailing.seller == Seller.telegram_id))
             .switch(ViewedMailing)
             .join(Mailing)
             .where(((ViewedMailing.buyer.is_null(False)) | (ViewedMailing.seller.is_null(False))) & (Mailing.is_sent == True) & (Mailing.id == mailing) & (ViewedMailing.mailing_id == mailing)))

    viewed_mailings = list(await manager.execute(viewed_mailings_query))
    if viewed_mailings:
        data_to_delete = dict()
        for viewed_mailing in viewed_mailings:
            if viewed_mailing.User:
                user_object = viewed_mailing.User
            elif viewed_mailing.Seller:
                user_object = viewed_mailing.Seller

            data_to_delete[user_object.telegram_id] = viewed_mailing.message_ids

        if data_to_delete:
            await manager.execute(ViewedMailing.delete().where(ViewedMailing.mailing_id == mailing))

            await manager.execute(Mailing.delete().where(Mailing.id == mailing.id))
        return data_to_delete
