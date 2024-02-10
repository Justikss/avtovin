import asyncio
import importlib
import logging
import traceback
from datetime import datetime, timedelta
from typing import List, Tuple, Optional

import aiocron
from aiogram import Bot
from peewee import IntegrityError

from config_data.config import mailing_interval
from database.tables.mailing import Mailing
# from utils.asyncio_tasks.invalid_tariffs_deleter import loader_module
from utils.middleware.exceptions_handler.middleware import ErrorHandler

mailing_requests_module = importlib.import_module('database.data_requests.mailing_requests')
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class MailingService:
    def __init__(self):
        self.mailing_tasks = {}
        self.cancelled_tasks = set()
        aiocron.crontab('0 0 * * *', func=self.cleanup_cancelled_tasks)

    @staticmethod
    def end_time_control(end_time):
        two_minutes_future_time = datetime.now() + timedelta(minutes=2)
        if end_time <= two_minutes_future_time:
            end_time = two_minutes_future_time
        return end_time

    async def schedule_mailing(self, bot: Bot):
        mailings = await mailing_requests_module.get_mailings_by_viewed_status(False)
        ic(mailings)
        for mailing in mailings:
            send_time = self.end_time_control(mailing.scheduled_time)
            if send_time > datetime.now():
                # Упрощенно, без конвертации в cron-формат для примера
                task_id = str(mailing.id)
                self.mailing_tasks[task_id] = mailing.scheduled_time
                logging.debug('Высылается(с loader) рассылка:%d в %s ', mailing.id)
                cron_string = send_time.strftime('%M %H %d %m *')

                aiocron.crontab(cron_string, func=self.send_scheduled_message_wrapper, args=(bot, mailing.id, task_id))


    async def send_scheduled_message_wrapper(self, bot: Bot, mailing, task_id=None):
        if not task_id:
            if isinstance(mailing, Mailing):
                task_id = mailing.id
            else:
                task_id = mailing
        ic(task_id, self.cancelled_tasks)

        if task_id in self.cancelled_tasks:
            logging.debug(f"Задача {task_id} отменена.")
            return
        ic()
        await self.send_scheduled_message(bot, mailing)

    async def cancel_mailing(self, mailing_id, from_deleting=False):
        task_id = str(mailing_id)
        self.cancelled_tasks.add(task_id)
        if not from_deleting:
            await mailing_requests_module.delete_mailing_action(mailing_id)
        logging.debug(f"Запланировано отменить задачу {task_id}.")

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


    def schedule_single_mailing(self, bot: Bot, mailing):
        scheduled_time = datetime.strptime(str(mailing.scheduled_time)[:-3], "%Y-%m-%d %H:%M")

        if scheduled_time > datetime.now():
            scheduled_time = self.end_time_control(scheduled_time)
            cron_string = scheduled_time.strftime('%M %H %d %m *')
            logging.debug('Запланирована рассылка:%d в %s ', mailing.id, scheduled_time)
            aiocron.crontab(cron_string, func=self.send_scheduled_message_wrapper, args=(bot, mailing.id))
        else:
            logging.debug('Отправляется незапланированная рассылка:%d в %s ', mailing.id, scheduled_time)
            asyncio.create_task(self.send_scheduled_message_wrapper(bot, mailing.id))


    async def send_scheduled_message(self, bot: Bot, mailing):
        logging.debug('Отправляется рассылка:%d', mailing)

        ic()
        ic(mailing)
        if not isinstance(mailing, Mailing):
            mailing = await mailing_requests_module.get_mailing_by_id(mailing)
            if not mailing:
                return
        recipients = await self.get_recipients(mailing.recipients_type)
        ic(mailing, recipients)
        if isinstance(recipients, tuple) and recipients[0]:
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
                    # traceback.print_exc()
                    pass
        else:
            # from database.data_requests.mailing_requests import update_mailing_status
            # await update_mailing_status(mailing)
            await self.cancel_mailing(mailing.id)
            return

    async def cleanup_cancelled_tasks(self):
        current_time = datetime.now()
        to_remove = {task_id for task_id in self.cancelled_tasks if self.mailing_tasks[task_id] < current_time}
        for task_id in to_remove:
            self.cancelled_tasks.remove(task_id)
            logging.debug(f"Очищен отменённый таск: {task_id}")

mailing_service = MailingService()