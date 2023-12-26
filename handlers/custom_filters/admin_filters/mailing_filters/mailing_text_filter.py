from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.utils.delete_message import delete_message


class MailingTextFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        ic()
        # Замена небезопасных символов на их экранированные версии
        modified_text = message.text.replace('<', '&lt;').replace('>', '&gt;')
        ic(modified_text)
        await delete_message(message, message.message_id)
        return {'modified_text': modified_text}
