import importlib

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import datetime

from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.input_mailing_data.input_date import \
    request_mailing_date_time
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.memory_storage_incorrect_controller import \
    incorrect
from handlers.utils.delete_message import delete_message


class DateTimeFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        config_module = importlib.import_module('config_data.config')

        memory_storage = await state.get_data()
        last_admin_answer = memory_storage.get('last_admin_answer')
        if last_admin_answer:
            await delete_message(message, last_admin_answer)

        try:
            mailing_datetime = datetime.datetime.strptime(message.text, config_module.MAILING_DATETIME_FORMAT)

            if mailing_datetime < datetime.datetime.now():
                await incorrect(state, message.message_id)
                await request_mailing_date_time(message, state, incorrect='(time)')
                return

            await delete_message(message, message.message_id)
            return {'mailing_datetime': str(mailing_datetime)}
        except (ValueError, TypeError):
            await incorrect(state, message.message_id)
            # await delete_message(message, message.message_id)
            await request_mailing_date_time(message, state, incorrect=True)  # Возвращаем False, если формат некорректен
