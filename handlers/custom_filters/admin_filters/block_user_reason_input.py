
import importlib
from typing import Dict, Any

from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, chat
import importlib

from config_data.config import max_contact_info_len, block_user_reason_text_len
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.user_ban.start_ban_process_input_reason import \
    input_ban_reason_handler
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON


class ControlInputUserBlockReason(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        escape_html_module = importlib.import_module('handlers.utils.escape_html_message')

        message_text = await escape_html_module.escape_html(message)
        message_len = len(message_text.replace(' ', ''))
        ic(message_len)
        if block_user_reason_text_len['min'] <= message_len \
                <= block_user_reason_text_len['max'] and not any(symbol in message.text for symbol in "<>"):

            await self.delete_last_admin_message(message, state)

            return {'reason': message_text.strip()}
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

        # lexicon_part = ADMIN_LEXICON['final_decision_ban_user']
        # lexicon_part['message_text'] = ADMIN_LEXICON['incorrect_input_block_reason'] + str(message_len)

        await input_ban_reason_handler(message, state, incorrect=message_len)
        await self.delete_last_incorrect_input(message, state)

    async def delete_last_admin_message(self, message: Message, state: FSMContext):
        try:
            ic()
            await message.chat.delete_message(message_id=message.message_id)
            ic()
        except TelegramBadRequest:
            pass