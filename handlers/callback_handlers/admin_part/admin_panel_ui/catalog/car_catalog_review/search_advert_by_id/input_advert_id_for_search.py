import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.admin_part_states.catalog_states.catalog_review_states import AdminCarCatalogSearchByIdStates

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


async def input_advert_id_for_search_admin_handler(request: CallbackQuery | Message, state: FSMContext, incorrect=False):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    if await state.get_state() != AdminCarCatalogSearchByIdStates.await_input_for_admin:
        await state.set_state(AdminCarCatalogSearchByIdStates.await_input_for_admin)

    lexicon_part, reply_mode = await get_lexicon_part_in_view_on_incorrect_flag(request, state, incorrect)

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='',
                                                    lexicon_part=lexicon_part, delete_mode=True,
                                                    reply_message=reply_mode)

    if isinstance(request, CallbackQuery):
        await request.answer()

async def get_lexicon_part_in_view_on_incorrect_flag(request, state, incorrect):
    reply_mode = None
    lexicon_code = 'search_advert_by_id_await_input'
    lexicon_part = Lexicon_module.CATALOG_LEXICON[lexicon_code]
    if incorrect:
        memory_storage = await state.get_data()
        if not memory_storage.get('incorrect_flag'):
            await state.update_data(incorrect_flag=True)
            ic(await state.update_data(last_admin_answer=request.message_id))
        lexicon_part['message_text'] = Lexicon_module.CATALOG_LEXICON[f'{lexicon_code}{incorrect}']
        if isinstance(request, Message):
            reply_mode = request.message_id
    return lexicon_part, reply_mode