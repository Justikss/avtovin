import importlib
from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message



async def main_menu(request: Union[CallbackQuery, Message], state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    redis_data = importlib.import_module('utils.redis_for_language')
    if await state.get_state():
        await state.clear()
    ic()
    await message_editor.travel_editor.edit_message(lexicon_key='main_menu', request=request, delete_mode=True)
    user_id = request.from_user.id
    redis_key = str(user_id) + ':user_state'
    await message_editor.redis_data.set_data(redis_key, value='buy')


