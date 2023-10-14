from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from handlers.callback_handlers.main_menu import travel_editor

from handlers.callback_handlers.language_callback_handler import redis_data

# from handlers.callback_handlers.backward_callback_handler import redis_data


async def search_auto_callback_handler(callback: CallbackQuery):
    await travel_editor.edit_message(lexicon_key='search_auto', request=callback)

async def search_configuration_handler(callback: CallbackQuery):
    await travel_editor.edit_message(lexicon_key='search_configuration', request=callback)
    user_id = callback.from_user.id
    redis_key = str(user_id) + ':cars_type'
    await redis_data.set_data(redis_key, callback.data)

