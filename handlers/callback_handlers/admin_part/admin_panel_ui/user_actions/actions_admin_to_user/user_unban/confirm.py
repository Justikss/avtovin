import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.banned_person_requests import BannedRequester
from handlers.callback_handlers.sell_part.seller_main_menu import try_get_free_tariff


async def handle_unban_to_system(callback, user_type, user_id):

    from utils.user_notification import send_notification
    from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action

    await send_notification(callback, user_status=f'unban:{user_type}', chat_id=user_id)

    await log_admin_action(callback.from_user.username,
                           f'unban_{user_type}',
                           f'{user_type}:{user_id}')

async def confirm_unblock_user(callback: CallbackQuery, state: FSMContext):
    Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    from handlers.utils.message_answer_without_callback import send_message_answer

    user = False
    seller = False

    memory_storage = await state.get_data()
    user_type = memory_storage.get('admin_review_user_mode')
    ic(user_type)
    if user_type == 'buyer':
        user_id = memory_storage.get('current_user_id')
        user = True
    else:
        user_type = 'seller'
        seller = True
        user_id = memory_storage.get('current_seller_id')
    unban_query = await BannedRequester.remove_ban(user_id,
                                              user=user, seller=seller)

    if unban_query:
        text = Lexicon_module.ADMIN_LEXICON['successfully']
        asyncio.create_task(handle_unban_to_system(callback, user_type, user_id))
        asyncio.create_task(try_get_free_tariff(callback, normal_status=True, user_id=user_id))

    else:
        text = Lexicon_module.ADMIN_LEXICON['unsuccessfully']

    await send_message_answer(callback, text, message=True)

    if user:
        from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_buyer import \
            output_buyer_profile

        await output_buyer_profile(callback, state)
    elif seller:
        from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_seller import \
            output_specific_seller_profile_handler

        await output_specific_seller_profile_handler(callback, state)
    else:
        from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person import \
            choose_specific_person_by_admin_handler

        await choose_specific_person_by_admin_handler(callback, state, first_call=False)