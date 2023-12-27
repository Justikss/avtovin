import asyncio
import importlib
from datetime import datetime
from typing import List

from aiogram import Bot

from config_data.config import MAILING_DATETIME_FORMAT, MODIFIED_MAILING_DATETIME_FORMAT
from database.data_requests.mailing_requests import retrieve_mailings_that_has_not_been_sent, update_mailing_status
from utils.mailing_heart.send_mailing_to_user import send_mailing


class MailingService:
    async def get_recipients(self, recipients_type: str) -> List[int]:
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

        return user_ids

    async def schedule_mailing(self, bot: Bot):
        mailings = await retrieve_mailings_that_has_not_been_sent()
        for mailing in mailings:
            if mailing.scheduled_time > datetime.now():
                delay = (mailing.scheduled_time - datetime.now()).total_seconds()
                asyncio.create_task(self.send_scheduled_message(bot, mailing, delay))

    async def send_scheduled_message(self, bot: Bot, mailing, delay):
        await asyncio.sleep(delay)
        recipients = await self.get_recipients(mailing.recipients_type)
        for recipient_id in recipients:
            try:
                await send_mailing(bot, mailing.media, mailing.text, recipient_id)
            except Exception:
                # Обработка исключений
                pass
            
        await update_mailing_status(mailing)

    async def schedule_single_mailing(self, bot: Bot, mailing):
        delay = (datetime.strptime(str(mailing.scheduled_time)[:-3], MODIFIED_MAILING_DATETIME_FORMAT) - datetime.now()).total_seconds()
        if delay > 0:
            asyncio.create_task(self.send_scheduled_message(bot, mailing, delay))