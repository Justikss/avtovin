import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils.get_user_name import get_user_name


async def output_buyer_profile(request: CallbackQuery | Message, state: FSMContext, user_id=None):
    person_requester_module = importlib.import_module('database.data_requests.person_requests')
    message_editor_module = importlib.import_module('handlers.message_editor')

    if isinstance(request, CallbackQuery):
        if request.data[-1].isdigit():
            user_id = request.data.split(':')[-1]
        else:
            memory_storage = await state.get_data()
            user_id = memory_storage.get('current_user_id')
    user_model = await person_requester_module.PersonRequester.get_user_for_id(user_id, user=True)
    if user_model:
        Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        ic()
        ic(user_id)
        await state.update_data(current_user_id=user_id)
        user_model = user_model[0]
        user_fullname, user_status = await get_user_name(user_model)
        lexicon_part = Lexicon_module.ADMIN_LEXICON['review_buyer_card']
        lexicon_part['message_text'] = lexicon_part['message_text'].format(full_name=user_fullname,
                                                                           phone_number=user_model.phone_number)

        await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='',
                                                                   lexicon_part=lexicon_part, dynamic_buttons=2, delete_mode=True)