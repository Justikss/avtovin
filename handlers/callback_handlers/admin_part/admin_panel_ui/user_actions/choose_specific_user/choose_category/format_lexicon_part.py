import importlib


async def choose_category_format_lexicon_part(state, lexicon_key):
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    memory_storage = await state.get_data()
    users_block_state = memory_storage.get('users_block_state')
    users_block_state_caption = lexicon_module.ADMIN_LEXICON.get(f'banned_users_caption:{users_block_state}')
    lexicon_part = lexicon_module.ADMIN_LEXICON[lexicon_key]
    lexicon_part['message_text'] = lexicon_part['message_text'].format(block_state=users_block_state_caption)

    return lexicon_part