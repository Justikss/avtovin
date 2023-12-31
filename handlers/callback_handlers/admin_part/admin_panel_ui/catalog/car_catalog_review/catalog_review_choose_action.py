import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from utils.lexicon_utils.Lexicon import CATALOG_LEXICON


async def choose_review_catalog_type_admin_handler(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    if await state.get_state():
        await state.clear()
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part=CATALOG_LEXICON['car_catalog_review_choose_category'],
                                                    dynamic_buttons=2)
    if isinstance(callback, CallbackQuery):
        await callback.answer()
