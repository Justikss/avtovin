
import importlib
from typing import Dict, Any

from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, chat
import importlib

from config_data.config import block_user_reason_text_len
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.car_catalog_review.catalog__specific_advert_actions.catalog_review__input_action_reason import \
    input_reason_to_close_advert_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.user_ban.start_ban_process_input_reason import \
    input_ban_reason_handler
from handlers.utils.delete_message import delete_message


class ControlInputUserBlockReason(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        escape_html_module = importlib.import_module('handlers.utils.escape_html_message')

        # message_text = await escape_html_module.escape_html(message)
        message_text = message.text
        message_len = len(message_text.replace(' ', ''))
        ic(message_len)
        if block_user_reason_text_len['min'] <= message_len \
                <= block_user_reason_text_len['max'] and not any(symbol in message.text for symbol in "<>"):

            await self.delete_last_admin_message(message, state)
            await state.update_data(reason=message_text.strip())
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

        current_state = str(await state.get_state())
        if current_state.startswith('AdminCarCatalogReviewStates'):
            await input_reason_to_close_advert_admin_handler(message, state, incorrect=message_len)
        else:
            await input_ban_reason_handler(message, state, incorrect=message_len)
        await self.delete_last_incorrect_input(message, state)

    async def delete_last_admin_message(self, message: Message, state: FSMContext):
        memory_storage = await state.get_data()
        last_admin_message = memory_storage.get('last_admin_answer')
        if last_admin_message:
            await delete_message(message, last_admin_message)
        await delete_message(message, message.message_id)
