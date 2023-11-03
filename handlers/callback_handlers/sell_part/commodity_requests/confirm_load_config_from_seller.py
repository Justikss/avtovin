from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

from config_data.config import ADMIN_CHAT
from utils.Lexicon import LexiconCommodityLoader, LEXICON

async def confirm_load_config_from_seller(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await state.clear()
    notification_string = await LexiconCommodityLoader.create_notification_for_seller(request_number='1')
    lexicon_part = LEXICON['seller_load_notification_button']
    for key, value in lexicon_part:
        notification_string[key] = value
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=notification_string)

    message_for_admin_chat = await LexiconCommodityLoader.get_output_string(mode='to_admins_from_' + callback.from_user.username)

    last_output_boot_config_string = await message_editor.redis_data.get_data(key=str(callback.from_user.id) + ':boot_config')
    boot_config_string_startswith = LexiconCommodityLoader.config_for_admins + callback.from_user.username + ' :'

    message_for_admin_chat = message_for_admin_chat.split('\n')
    message_for_admin_chat[0] = boot_config_string_startswith

    await callback.message.bot.send_message(chat_id=ADMIN_CHAT, text=message_for_admin_chat)