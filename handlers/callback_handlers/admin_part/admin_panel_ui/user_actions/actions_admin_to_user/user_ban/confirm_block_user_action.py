from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.banned_person_requests import BannedRequester
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.user_ban.utils.delete_last_user_messages import \
    wipe_user_chat_history
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
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action
from utils.user_notification import send_notification


async def confirm_user_block_action(callback: CallbackQuery, state: FSMContext):
    current_state = str(await state.get_state())
    memory_storage = await state.get_data()

    user_id = memory_storage.get('user_id')
    user = True if current_state.startswith('BuyerReviewStates') else False
    seller = True if current_state.startswith('SellerReviewStates') else False
    user_status = 'seller_ban' if current_state.startswith('SellerReviewStates') else 'buyer_ban'

    try:
        ban_query = await BannedRequester.set_ban(callback, user_id, reason=memory_storage.get('reason'),
                                                  user=user, seller=seller)
        if ban_query:
            user_mode = 'seller' if seller else 'buyer'
            await log_admin_action(callback.from_user.username, f'ban_{user_mode}', ban_query)
            await callback.answer(ADMIN_LEXICON['user_block_success'])
            await wipe_user_chat_history(callback, state, user_id, user=user, seller=seller)
            await send_notification(callback, user_status=user_status, chat_id=user_id, ban_reason=memory_storage.get('reason'))
            return await choose_user_category_by_admin_handler(callback, state)

    except AdminDoesNotExistsError:
        return await admin_does_not_exists_handler(callback)

    except UserNonExistsError:
        await callback.answer(ADMIN_LEXICON['user_non_active'])
        await backward_from_user_profile_review(callback, state)