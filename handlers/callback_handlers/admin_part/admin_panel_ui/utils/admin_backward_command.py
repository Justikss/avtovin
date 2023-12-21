from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.tariff_for_seller.checkout_tariff_by_admin import \
    checkout_seller_tariff_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.tariff_for_seller.choose_tariff_for_seller import \
    checkout_tariff_for_seller_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.user_ban.start_ban_process_input_reason import \
    input_ban_reason_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_category.choose_seller_category import \
    choose_seller_category_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_category.choose_users_category import \
    choose_user_category_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person import \
    choose_specific_person_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_seller import \
    output_specific_user_profile_handler
from handlers.callback_handlers.buy_part.language_callback_handler import set_language


async def admin_backward_command_handler(callback: CallbackQuery, state: FSMContext):
    backward_mode = callback.data.split(':')[-1]

    if backward_mode == 'seller_list_to_admin':
        await choose_seller_category_by_admin_handler(callback)

    elif backward_mode == 'admin_main_menu':
        await set_language(callback, set_languange=False)

    elif backward_mode in ('choose_seller_category', 'user_list_to_admin'):
        await choose_user_category_by_admin_handler(callback, state)

    elif backward_mode == 'user_profile_review':
        await choose_specific_person_by_admin_handler(callback, state, delete_redis_pagination_key=False,
                                                      first_call=False)

    elif backward_mode in ('review_seller_tariff', 'input_ban_reason', 'review_result_profile_protocol'):
        await output_specific_user_profile_handler(callback, state)

    elif backward_mode in ('choose_tariff_for_seller', 'tariff_for_seller_review', 'reset_seller_tariff'):
        await checkout_seller_tariff_by_admin_handler(callback, state)

    elif backward_mode == 'tariff_to_seller_pre_confirm_moment':
        await checkout_tariff_for_seller_by_admin_handler(callback, state)

    elif backward_mode == 'final_confirm_block_user':
        await input_ban_reason_handler(callback, state)
