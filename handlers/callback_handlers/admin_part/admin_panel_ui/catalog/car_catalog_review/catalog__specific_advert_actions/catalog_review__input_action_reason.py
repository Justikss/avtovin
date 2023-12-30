import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils.lexicon_utils.Lexicon import CATALOG_LEXICON, ADMIN_LEXICON
from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import catalog_captions


async def input_reason_lexicon_part_modification(request: CallbackQuery| Message, state: FSMContext, incorrect):
    if isinstance(request, CallbackQuery) and 'catalog_action__' in request.data:
        acton_subject = request.data.split('_')[-2]
        await state.update_data(advert_action_subject=acton_subject)
    else:
        memory_storage = await state.get_data()
        acton_subject = memory_storage.get('advert_action_subject')

    lexicon_part = CATALOG_LEXICON['catalog_close_advert__input_reason']
    lexicon_part['message_text'] = lexicon_part['message_text'].format(acton_subject=catalog_captions[f'to_{acton_subject}'])
    if incorrect:
        lexicon_part['message_text'] += ADMIN_LEXICON['incorrect_input_block_reason'] + str(incorrect)
    return lexicon_part

async def input_reason_to_close_advert_admin_handler(request: CallbackQuery| Message, state: FSMContext, incorrect=False):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    lexicon_part = await input_reason_lexicon_part_modification(request, state, incorrect)
    if incorrect:
        reply_mode = request.message_id
    else:
        reply_mode = None

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='',
                                                    lexicon_part=lexicon_part, reply_message=reply_mode)

    if isinstance(request, CallbackQuery):
        await request.answer()
