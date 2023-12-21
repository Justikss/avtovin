import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.person_requests import PersonRequester
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person import \
    choose_specific_person_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.utils.backward_from_user_output import \
    backward_from_user_profile_review
from utils.get_user_name import get_user_name
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON
from utils.lexicon_utils.admin_lexicon import BanUser

async def get_user_entity(callback: CallbackQuery, state: FSMContext):
    current_state = str(await state.get_state())
    memory_storage = await state.get_data()

    user = True if current_state.startswith('BuyerReviewStates') else False
    seller = True if current_state.startswith('SellerReviewStates') else False

    if seller:
        user_id = memory_storage.get('current_seller_id')
    elif user:
        user_id = memory_storage.get('current_user_id')
    else:
        user_id = None

    ic(seller, user, user_id)
    if user_id:
        await state.update_data(user_id=user_id)
        user_model = await PersonRequester.get_user_for_id(user_id, user=user, seller=seller)
        ic(user_model)
        if user_model:
            user_name, user_entity = await get_user_name(user_model)
            return user_name, user_entity

    return False

async def input_ban_reason_handler(callback: CallbackQuery, state: FSMContext):
    message_editor_module = importlib.import_module('handlers.message_editor')

    user_data = await get_user_entity(callback, state)
    if user_data:
        user_name, user_entity = user_data
        await state.update_data(user_entity=user_entity)
        await state.update_data(user_name=user_name)
        lexicon_class = BanUser.InputReason(user_entity, user_name)
        lexicon_part = lexicon_class.lexicon_part
        await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='',
                                                       lexicon_part=lexicon_part)
    else:
        await callback.answer(ADMIN_LEXICON['action_non_actuality'])
        await backward_from_user_profile_review(callback, state)
