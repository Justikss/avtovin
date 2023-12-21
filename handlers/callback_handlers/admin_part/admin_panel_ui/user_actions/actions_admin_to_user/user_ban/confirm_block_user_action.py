from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.banned_person_requests import BannedRequester
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_category.choose_users_category import \
    choose_user_category_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person import \
    choose_specific_person_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_does_not_exists_handler import \
    admin_does_not_exists_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.utils.backward_from_user_output import \
    backward_from_user_profile_review
from utils.custom_exceptions.database_exceptions import AdminDoesNotExistsError, UserNonExistsError
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON


async def confirm_user_block_action(callback: CallbackQuery, state: FSMContext):
    current_state = str(await state.get_state())
    memory_storage = await state.get_data()

    user_id = memory_storage.get('user_id')
    user = True if current_state.startswith('BuyerReviewStates') else False
    seller = True if current_state.startswith('SellerReviewStates') else False

    try:
        ban_query = await BannedRequester.set_ban(callback, user_id, user=user, seller=seller)
        if ban_query:
            await callback.answer(ADMIN_LEXICON['user_block_success'])
            return await choose_user_category_by_admin_handler(callback, state)

    except AdminDoesNotExistsError:
        return await admin_does_not_exists_handler(callback)

    except UserNonExistsError:
        await callback.answer(ADMIN_LEXICON['user_non_active'])
        await backward_from_user_profile_review(callback, state)