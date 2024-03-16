import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_category.format_lexicon_part import \
    choose_category_format_lexicon_part

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт


async def choose_user_block_status(request: Message | CallbackQuery, state: FSMContext):

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='',
                                                    lexicon_part=await choose_category_format_lexicon_part
                                                        (state, 'choose_user_block_category'),
                                                    dynamic_buttons=1)

