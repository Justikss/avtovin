import asyncio
import importlib
import logging
import traceback
from datetime import datetime
from typing import List, Tuple, Optional

from aiogram import Bot
from peewee import IntegrityError

from config_data.config import mailing_interval
from utils.middleware.exceptions_handler.middleware import ErrorHandler

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
                ic(delay)
                task = asyncio.create_task(self.send_scheduled_message(bot, mailing, delay))
                self.mailing_tasks[mailing.id] = task
            else:
                delay = 1
                ic(delay)
                ic(mailing)
                asyncio.create_task(self.send_scheduled_message(bot, mailing, delay))

    async def send_scheduled_message(self, bot: Bot, mailing, delay):

        try:
            await asyncio.sleep(delay)
            # Отправка сообщения
        except asyncio.CancelledError:
            # Обработка отмены задачи
            return
        recipients = await self.get_recipients(mailing.recipients_type)
        ic(mailing, recipients)
        if recipients:
            from utils.mailing_heart.send_mailing_to_user import send_mailing

            recipients, users_recipient = recipients
            buyer_recipient, seller_recipient = users_recipient
            mailing_data = dict()
            ic(recipients, users_recipient, buyer_recipient, seller_recipient)
            for recipient_id in recipients:
                try:
                    chat_id_to_message_ids = await send_mailing(bot, mailing.media, mailing.text, recipient_id)
                    if chat_id_to_message_ids:
                        mailing_data.update(chat_id_to_message_ids)

                    await asyncio.sleep(mailing_interval)

                except Exception as e:
                    trace_back = await ErrorHandler().format_traceback()
                    logging.error('Ошибка при рассылке по ID %d: %s\n%s\n%s\n%s', recipient_id, e,
                                  e.message if hasattr(e, 'message') else '',
                                  e.args if e.args else '',
                                  trace_back)

            ic(mailing, mailing_data)

            if mailing_data:
                try:
                    await mailing_requests_module.view_mailing_action(mailing_data, mailing,
                                                                      buyer_recipient, seller_recipient)
                except IntegrityError:
                    traceback.print_exc()
                    pass

    async def schedule_single_mailing(self, bot: Bot, mailing):
        config_module = importlib.import_module('config_data.config')

        delay = (datetime.strptime(str(mailing.scheduled_time)[:-3], config_module\
                                   .MODIFIED_MAILING_DATETIME_FORMAT) - datetime.now()).total_seconds()
        if delay > 0:
            task = asyncio.create_task(self.send_scheduled_message(bot, mailing, delay))
            self.mailing_tasks[mailing.id] = task

    async def cancel_mailing(self, mailing_id):
        task = self.mailing_tasks.get(mailing_id)
        if task:
            task.cancel()
            del self.mailing_tasks[mailing_id]  # Удаление задачи из словаря

mailing_service = MailingService()