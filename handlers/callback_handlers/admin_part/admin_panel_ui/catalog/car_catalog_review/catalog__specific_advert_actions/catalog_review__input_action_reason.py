import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.admin_part_states.catalog_states.catalog_review_states import AdminCarCatalogReviewStates

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def input_reason_lexicon_part_modification(request: CallbackQuery| Message, state: FSMContext, incorrect):
    if isinstance(request, CallbackQuery) and 'catalog_action__' in request.data:
        acton_subject = request.data.split('_')[-2]
        await state.update_data(advert_action_subject=acton_subject)
    else:
        memory_storage = await state.get_data()
        acton_subject = memory_storage.get('advert_action_subject')

    lexicon_part = Lexicon_module.CATALOG_LEXICON['catalog_close_advert__input_reason']
    lexicon_part['message_text'] = lexicon_part['message_text'].format(acton_subject=Lexicon_module.catalog_captions[f'to_{acton_subject}'])
    if incorrect:
        lexicon_part['message_text'] += f'''\n{Lexicon_module.ADMIN_LEXICON['incorrect_input_block_reason']}{incorrect}'''
    return lexicon_part

async def input_reason_to_close_advert_admin_handler(request: CallbackQuery| Message, state: FSMContext, incorrect=False):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await state.set_state(AdminCarCatalogReviewStates.await_input_reason_action)
    lexicon_part = await input_reason_lexicon_part_modification(request, state, incorrect)
    if incorrect:
        reply_mode = request.message_id
    else:
        reply_mode = None

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='',
                                                    lexicon_part=lexicon_part, reply_message=reply_mode,
                                                    delete_mode=bool(reply_mode) is True)


