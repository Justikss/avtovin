from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.input_mailing_data.input_text import \
    enter_mailing_text
from handlers.utils.delete_message import delete_message


class MailingTextFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        from utils.oop_handlers_engineering.update_handlers.base_objects.utils_objects.incorrect_adapter import \
            IncorrectAdapter
        incorrect_manager = IncorrectAdapter()
        ic()
        # Замена небезопасных символов на их экранированные версии
        modified_text = message.text.replace('<', '&lt;').replace('>', '&gt;')
        ic(modified_text)
        from config_data.config import mailing_text_max_len

        await incorrect_manager.try_delete_incorrect_message(message, state)

        if len(modified_text) < mailing_text_max_len:
            await delete_message(message, message.message_id)
            return {'modified_text': modified_text}
        else:
            await state.update_data(last_admin_answer=message.message_id)
            await state.update_data(admin_incorrect_flag=True)
            await enter_mailing_text(message, state, True)
