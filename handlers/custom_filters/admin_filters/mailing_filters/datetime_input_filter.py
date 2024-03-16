import importlib
import traceback

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
        from config_data.config import datetime_input_max_len
        if len(message.text) > datetime_input_max_len:
            await incorrect(state, message.message_id)

            await request_mailing_date_time(message, state, incorrect=True)  # Возвращаем False, если формат некорректен
            return
        else:
            try:
                print(message.text)
                mailing_datetime = datetime.datetime.strptime(message.text, '%d-%m-%Y %H:%M')
                ic(mailing_datetime.__class__.__name__)
                print(mailing_datetime)
                if mailing_datetime < datetime.datetime.now():
                    await incorrect(state, message.message_id)
                    await request_mailing_date_time(message, state, incorrect='(time)')
                    return

                await delete_message(message, message.message_id)
                mailing_datetime = mailing_datetime.strftime('%d-%m-%Y %H:%M')
                return {'mailing_datetime': mailing_datetime}
            except (ValueError, TypeError):
                traceback.print_exc()
                await incorrect(state, message.message_id)
                # await delete_message(message, message.message_id)
                await request_mailing_date_time(message, state, incorrect=True)  # Возвращаем False, если формат некорректен
