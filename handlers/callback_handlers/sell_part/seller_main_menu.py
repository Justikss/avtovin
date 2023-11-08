from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

from utils.Lexicon import LEXICON
from handlers.callback_handlers.buy_part.show_offers_history import try_delete_notification


async def seller_main_menu(callback: CallbackQuery, bot=None):
    message_editor_module = importlib.import_module('handlers.message_editor')
    redis_data = importlib.import_module('utils.redis_for_language')

    await try_delete_notification(callback=callback, user_status='seller')

    await redis_data.redis_data.delete_key(key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')

    lexicon_code = 'seller_main_menu'
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key=lexicon_code, bot=bot)

    user_id = callback.from_user.id
    redis_key = str(user_id) + ':user_state'
    await redis_data.redis_data.set_data(redis_key, value='sell')