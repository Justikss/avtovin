from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import datetime

from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.input_mailing_data.input_media import \
    request_mailing_media
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.memory_storage_incorrect_controller import \
    incorrect
from handlers.callback_handlers.hybrid_part.utils.media_group_collector import collect_and_send_mediagroup
from handlers.utils.delete_message import delete_message


class MediaFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        memory_storage = await state.get_data()
        last_admin_answer = memory_storage.get('last_admin_answer')
        if last_admin_answer:
            await delete_message(message, last_admin_answer)

        if message.text:
            await incorrect(state, message.message_id)
            # await delete_message(message, message.message_id)
            await request_mailing_media(message, state, incorrect=True)  # Возвращаем False, если формат некорректен
        else:
            await delete_message(message, message.message_id)
            return True