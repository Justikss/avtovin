import asyncio
import importlib
import traceback
from datetime import datetime
from typing import List, Tuple, Optional

from aiogram import Bot
from peewee import IntegrityError

from config_data.config import MAILING_DATETIME_FORMAT, MODIFIED_MAILING_DATETIME_FORMAT
from utils.mailing_heart.send_mailing_to_user import send_mailing

mailing_requests_module = importlib.import_module('database.data_requests.mailing_requests')

class MailingService:
    def __init__(self):
        self.mailing_tasks = {}

    async def get_recipients(self, recipients_type: str) -> Tuple[Optional[List[int]], Tuple[bool, bool]]:
        """
        Возвращает список идентификаторов пользователей для рассылки.
        """
        person_requester_module = importlib.import_module('database.data_requests.person_requests')

        get_users = False
        get_sellers = False
        if recipients_type == 'buyers':
            get_users = True
        elif recipients_type == 'sellers':
            get_sellers = True
        elif recipients_type == 'all_users':
            pass
        else:
            raise ValueError("Неверный тип получателей")

        user_ids = await person_requester_module.PersonRequester.retrieve_all_ids(user=get_users, seller=get_sellers)

        return user_ids, (get_users, get_sellers)

    async def schedule_mailing(self, bot: Bot):
        mailings = await mailing_requests_module.get_mailings_by_viewed_status(False)
        ic(mailings)
        for mailing in mailings:
            ic(mailing.scheduled_time)
            if mailing.scheduled_time > datetime.now():
                delay = (mailing.scheduled_time - datetime.now()).total_seconds()
                task = asyncio.create_task(self.send_scheduled_message(bot, mailing, delay))
                self.mailing_tasks[mailing.id] = task
            else:
                delay = 1
                asyncio.create_task(self.send_scheduled_message(bot, mailing, delay))

    async def send_scheduled_message(self, bot: Bot, mailing, delay):

        try:
            await asyncio.sleep(delay)
            # Отправка сообщения
        except asyncio.CancelledError:
            # Обработка отмены задачи
            return
        recipients = await self.get_recipients(mailing.recipients_type)
        if recipients:
            recipients, users_recipient = recipients
            buyer_recipient, seller_recipient = users_recipient
            mailing_data = dict()
            for recipient_id in recipients:
                chat_id_to_message_ids = await send_mailing(bot, mailing.media, mailing.text, recipient_id)
                if chat_id_to_message_ids:
                    mailing_data.update(chat_id_to_message_ids)

            await mailing_requests_module.update_mailing_status(mailing)
            if mailing_data:
                ic(mailing_data)
                try:
                    await mailing_requests_module.view_mailing_action(mailing_data, mailing,
                                                                      buyer_recipient, seller_recipient)
                except IntegrityError:
                    traceback.print_exc()
                    pass

    async def schedule_single_mailing(self, bot: Bot, mailing):
        delay = (datetime.strptime(str(mailing.scheduled_time)[:-3], MODIFIED_MAILING_DATETIME_FORMAT) - datetime.now()).total_seconds()
        if delay > 0:
            task = asyncio.create_task(self.send_scheduled_message(bot, mailing, delay))
            self.mailing_tasks[mailing.id] = task

    async def cancel_mailing(self, mailing_id):
        task = self.mailing_tasks.get(mailing_id)
        if task:
            task.cancel()
            del self.mailing_tasks[mailing_id]  # Удаление задачи из словаря

mailing_service = MailingService()