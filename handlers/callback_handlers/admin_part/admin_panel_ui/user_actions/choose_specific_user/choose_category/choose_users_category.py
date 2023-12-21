import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from utils.lexicon_utils.Lexicon import ADMIN_LEXICON


async def choose_user_category_by_admin_handler(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    if await state.get_state():
        await state.clear()

    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part=ADMIN_LEXICON['select_user_category'])