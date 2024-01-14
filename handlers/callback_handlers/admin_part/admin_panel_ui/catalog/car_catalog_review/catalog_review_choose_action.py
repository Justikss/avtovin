import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def choose_review_catalog_type_admin_handler(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    if await state.get_state():
        await state.clear()
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part=Lexicon_module\
                                                    .CATALOG_LEXICON['car_catalog_review_choose_category'],
                                                    dynamic_buttons=2, delete_mode=True)
    if isinstance(callback, CallbackQuery):
        await callback.answer()
