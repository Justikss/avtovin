from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.lexicon_utils.Lexicon import ADMIN_LEXICON


async def incorrect_controller(message: Message, state: FSMContext, incorrect, lexicon_key):
    ic(lexicon_key)
    lexicon_part = ADMIN_LEXICON[lexicon_key]
    if not incorrect:
        reply_mode = None
    else:
        reply_mode = message.message_id
        lexicon_part['message_text'] = ADMIN_LEXICON[f'{lexicon_key}(incorrect)']
    return lexicon_part, reply_mode

async def get_delete_mode(state: FSMContext, incorrect):
    if not incorrect:
        memory_storage = await state.get_data()
        delete_mode = memory_storage.get('admin_incorrect_flag') is True
        ic(delete_mode, memory_storage.get('admin_incorrect_flag'))
        if delete_mode:
            await state.update_data(admin_incorrect_flag=False)
    else:
        delete_mode = False
    return delete_mode