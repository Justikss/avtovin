import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_category.format_lexicon_part import \
    choose_category_format_lexicon_part

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


async def choose_seller_category_by_admin_handler(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    # if await state.get_state():
    #     await state.clear()

    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part=await choose_category_format_lexicon_part(
                                                        state, 'select_seller_category'))