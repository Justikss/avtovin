import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from states.hybrid_choose_states import HybridChooseStates


# from handlers.callback_handlers.backward_callback_handler import redis_data


async def search_auto_callback_handler(callback: CallbackQuery):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    await message_editor.travel_editor.edit_message(lexicon_key='search_car', request=callback)

    redis_key = str(callback.from_user.id) + ':last_lexicon_code'
    await message_editor.redis_data.set_data(redis_key, 'search_car')

async def search_configuration_handler(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await message_editor.travel_editor.edit_message(lexicon_key='search_configuration', request=callback, lexicon_cache=False)
    user_id = callback.from_user.id
    redis_key = str(user_id) + ':cars_type'
    await message_editor.redis_data.set_data(redis_key, callback.data)
    await state.set_state(HybridChooseStates.select_brand)

