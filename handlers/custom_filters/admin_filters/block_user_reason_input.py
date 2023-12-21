
import importlib

from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, chat
import importlib

from config_data.config import max_contact_info_len, block_user_reason_text_len
from database.data_requests.person_requests import PersonRequester
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON


class ControlInputUserBlockReason(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):

        message_len = len(message.text.replace(' ', ''))
        ic(message_len)
        if block_user_reason_text_len['min'] <= message_len \
                <= block_user_reason_text_len['max']:

            await self.delete_last_admin_message(message, state)

            return {'reason': message.text.strip()}
        else:
            await state.update_data(incorrect_flag=True)
            await self.send_incorrect_notification(message, state, message_len)

    async def delete_last_incorrect_input(self, message: Message, state: FSMContext):
        memory_storage = await state.get_data()
        last_answer = memory_storage.get('last_admin_answer')
        if last_answer:
            try:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=last_answer)
            except TelegramBadRequest:
                pass

        await state.update_data(last_admin_answer=message.message_id)

    async def send_incorrect_notification(self, message: Message, state: FSMContext, message_len):
        message_editor_module = importlib.import_module('handlers.message_editor')

        lexicon_part = ADMIN_LEXICON['final_decision_ban_user']
        lexicon_part['message_text'] = ADMIN_LEXICON['incorrect_input_block_reason'] + str(message_len)

        await message_editor_module.travel_editor.edit_message(request=message, lexicon_key='',
                                                               lexicon_part=lexicon_part, reply_message=message.message_id, delete_mode=True)
        await self.delete_last_incorrect_input(message, state)

    async def delete_last_admin_message(self, message: Message, state: FSMContext):
        try:
            ic()
            await message.chat.delete_message(message_id=message.message_id)
            ic()
        except TelegramBadRequest:
            pass