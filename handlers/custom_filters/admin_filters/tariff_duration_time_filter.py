import re
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.memory_storage_incorrect_controller import \
    incorrect
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_tariff_data import \
    process_write_tariff_feedbacks_residual
from handlers.utils.delete_message import delete_message


class TimeDurationFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        # Проверяем, соответствует ли сообщение формату "лет:месяцев:дней"
        result = bool(re.match(r'^\d+:\d+:\d+$', message.text))
        ic(result)
        memory_storage = await state.get_data()

        last_admin_answer = memory_storage.get('last_admin_answer')
        if last_admin_answer:
            await delete_message(message, last_admin_answer)
        if (not result) or (await self.input_is_null(message.text)):
            await incorrect(state, message.message_id)
            await process_write_tariff_feedbacks_residual(message, state, incorrect=True)
        else:
            await delete_message(message, message.message_id)
            return result

    async def input_is_null(self, text):
        clear_time = text.replace(':', ' ').split()
        for time_part in clear_time:
            for number in time_part:
                if number != '0':
                    return False
        return True
