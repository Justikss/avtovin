import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery





async def choose_user_category_by_admin_handler(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    memory_storage = await state.get_data()

    if callback.data.startswith('user_block_status:'):
        users_block_state = callback.data.split(':')[-1]
        await state.update_data(users_block_state=users_block_state)
    else:
        users_block_state = memory_storage.get('users_block_state')
    ic(users_block_state)
    users_block_state_caption = lexicon_module.ADMIN_LEXICON.get(f'banned_users_caption:{users_block_state}')
    lexicon_part = lexicon_module.ADMIN_LEXICON['select_user_category']
    lexicon_part['message_text'] = lexicon_part['message_text'].format(block_state=users_block_state_caption)

    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part=lexicon_part,
                                                    dynamic_buttons=2)