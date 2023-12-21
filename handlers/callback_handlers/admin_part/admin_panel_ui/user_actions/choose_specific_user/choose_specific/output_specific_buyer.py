import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.person_requests import PersonRequester
from utils.get_user_name import get_user_name
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON


async def output_buyer_profile(callback: CallbackQuery, state: FSMContext):
    message_editor_module = importlib.import_module('handlers.message_editor')

    user_id = callback.data.split(':')[-1]

    user_model = await PersonRequester.get_user_for_id(user_id, user=True)
    if user_model:
        ic()
        ic(user_id)
        await state.update_data(current_user_id=user_id)
        user_model = user_model[0]
        user_fullname, user_status = await get_user_name(user_model)
        lexicon_part = ADMIN_LEXICON['review_buyer_card']
        lexicon_part['message_text'] = lexicon_part['message_text'].format(full_name=user_fullname,
                                                                           phone_number=user_model.phone_number)

        await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='',
                                                                   lexicon_part=lexicon_part, dynamic_buttons=2)