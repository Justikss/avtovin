import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


from utils.get_user_name import get_user_name

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


async def get_lexicon_part(user_model, user_type):
    from utils.lexicon_utils.admin_lexicon.admin_lexicon import admin_class_mini_lexicon

    user_model = user_model[0]
    lexicon_part = Lexicon_module.ADMIN_LEXICON['unban_confirmation']

    user_name = await get_user_name(user_model)
    if isinstance(user_name, tuple):
        user_name = user_name[0]
    lexicon_key = ''
    match user_type:
        case 'legal':
            lexicon_key = 'ban_user_input_reason_dealership'

        case 'natural':
            lexicon_key = 'ban_user_input_reason_seller'

        case 'buyer':
            lexicon_key = 'ban_user_input_reason_buyer'

    user_entity = f'''<i>{admin_class_mini_lexicon.get(lexicon_key).replace(' {name}', '')}</i> <b>{user_name}</b>'''

    lexicon_part['message_text'] = lexicon_part['message_text'].format(user_entity=user_entity)

    return lexicon_part

async def user_unban_confirmation(callback: CallbackQuery, state: FSMContext):
    message_editor_module = importlib.import_module('handlers.message_editor')
    from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person import \
        choose_specific_person_by_admin_handler

    memory_storage = await state.get_data()
    user_type = memory_storage.get('admin_review_user_mode')

    person_requester_module = importlib.import_module('database.data_requests.person_requests')
    if user_type == 'buyer':
        user_id = memory_storage.get('current_user_id')
    else:
        user_id = memory_storage.get('current_seller_id')
    ic(user_type, user_id)

    user_model = await person_requester_module.PersonRequester.get_user_for_id(user_id, user=user_type == 'buyer',
                                                                               seller=user_type != 'buyer')
    if user_model:
        lexicon_part = await get_lexicon_part(user_model, user_type)
        await message_editor_module.travel_editor.edit_message(request=callback,
                                                               lexicon_part=lexicon_part,
                                                               lexicon_key='')


    else:
        if isinstance(callback, CallbackQuery):
            await callback.answer(Lexicon_module.ADMIN_LEXICON['user_non_active'])
        await choose_specific_person_by_admin_handler(callback, state, first_call=False)



