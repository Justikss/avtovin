import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.choose_advertisement_action import \
    choose_advertisement_action
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.review_inputted_data import \
    request_review_mailing_data
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.choose_mailing_action import \
    request_choose_mailing_action
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.mailing_storage.choose_specific_type import \
    request_choose_mailing_type
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.car_catalog_review.catalog__specific_advert_actions.catalog_review__input_action_reason import \
    input_reason_to_close_advert_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.car_catalog_review.catalog__specific_advert_actions.choose_specific_action import \
    choose_specific_advert_action_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.car_catalog_review.catalog_review_choose_action import \
    choose_review_catalog_type_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.car_catalog_review.output_choose.output_choose_brand_to_catalog_review import \
    choose_review_catalog_brand_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.choose_catalog_action import \
    choose_catalog_action_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.car_catalog_review.search_advert_by_id.input_advert_id_for_search import \
    input_advert_id_for_search_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_tariff_data import process_tariff_cost, \
    process_write_tariff_feedbacks_residual, process_write_tariff_cost
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.output_specific_tariff import \
    output_specific_tariff_for_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.output_tariff_list import \
    output_tariffs_for_admin
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.tariff_for_seller.checkout_tariff_by_admin import \
    checkout_seller_tariff_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.tariff_for_seller.choose_tariff_for_seller import \
    checkout_tariff_for_seller_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_category.choose_seller_category import \
    choose_seller_category_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_category.choose_users_category import \
    choose_user_category_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_buyer import \
    output_buyer_profile
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_seller import \
    output_specific_seller_profile_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_pagination import AdminPaginationOutput
from handlers.callback_handlers.buy_part.language_callback_handler import set_language
from handlers.utils.message_answer_without_callback import send_message_answer
from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import catalog_captions
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog import advert_parameters


async def admin_backward_command_handler(callback: CallbackQuery, state: FSMContext):
    input_reason_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.user_ban.start_ban_process_input_reason')
    choose_specific_person_by_admin_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person')
    backward_mode = callback.data.split(':')[-1]

    handler_class = None
    current_state = str(await state.get_state())
    memory_storage = await state.get_data()

    match backward_mode:

        case 'seller_list_to_admin':
            await choose_seller_category_by_admin_handler(callback, state)

        case 'admin_main_menu':
            await set_language(callback, set_languange=False)

        case 'choose_seller_category' | 'user_list_to_admin':
            await choose_user_category_by_admin_handler(callback, state)

        case 'user_profile_review' | 'input_name_to_search':
            await choose_specific_person_by_admin_module.choose_specific_person_by_admin_handler(
                callback,
                state,
                delete_redis_pagination_key=False,
                first_call=False)

        case 'review_seller_tariff' | 'input_ban_reason' | 'review_result_profile_protocol' | 'check_seller_statistic_values' if current_state.startswith('SellerReviewStates'):
            await output_specific_seller_profile_handler(callback, state)

        case 'input_ban_reason' if current_state.startswith('BuyerReviewStates'):
            await output_buyer_profile(callback, state)

        case 'choose_tariff_for_seller' | 'tariff_for_seller_review' | 'reset_seller_tariff':
            await checkout_seller_tariff_by_admin_handler(callback, state)

        case 'tariff_to_seller_pre_confirm_moment':
            await checkout_tariff_for_seller_by_admin_handler(callback, state)

        case 'final_confirm_block_user':
            await input_reason_module.input_ban_reason_handler(callback, state)

        case 'input_tariff_cost' | 'check_tariff_info':
            await output_tariffs_for_admin(callback, state)

        case 'input_tariff_feedbacks':
            await process_tariff_cost(callback, state)

        case 'input_tariff_duration_time':
            await process_write_tariff_cost(callback, state)

        case 'input_tariff_name':
            await process_write_tariff_feedbacks_residual(callback, state)

        case 'confirm_delete_tariff_action' | 'edit_tariff':
            await output_specific_tariff_for_admin_handler(callback, state, from_backward=True)

        case 'input_mailing_data':
            edit_mailing_flag = memory_storage.get('can_edit_mailing_flag')
            ic(edit_mailing_flag)
            ic(current_state)
            if not edit_mailing_flag or current_state in ('MailingStates:edit_inputted_data', 'MailingStates:confirmation'):
                await request_choose_mailing_action(callback, state)
            else:
                await request_review_mailing_data(callback, state)

        case 'choose_mailing_action':
            await choose_advertisement_action(callback, state)

        case 'choose_review_mailing_type':
            await request_choose_mailing_action(callback, state)

        case 'review_mailings':
            await request_choose_mailing_type(callback, state)

        case 'choose_catalog_review_advert_type' | 'advert_parameters_choose_state':
            await choose_catalog_action_admin_handler(callback, state)

        case 'catalog_review_choose_brand' | 'await_input_id_to_search_advert':
            await choose_review_catalog_type_admin_handler(callback, state)

        case 'review_specific_advert_catalog':
            if current_state.startswith('AdminCarCatalogReviewStates'):
                await choose_review_catalog_brand_admin_handler(callback, state)
            elif current_state.startswith('AdminCarCatalogSearchByIdStates'):
                await input_advert_id_for_search_admin_handler(callback, state)

        case 'catalog__choose_specific_advert_action' | 'to_catalog_review_adverts':
            if await AdminPaginationOutput.output_page(callback, state, None) is False:
                await send_message_answer(callback, catalog_captions['inactive_advert_or_seller'])
                if await choose_review_catalog_brand_admin_handler(callback, state) is False:
                    await choose_review_catalog_type_admin_handler(callback, state)

        case 'catalog_review_close_action_confirmation':
            await input_reason_to_close_advert_admin_handler(callback, state, False)

        case 'input_reason_to_close_advert':
            await choose_specific_advert_action_admin_handler(callback, state)

        case 'choose_second_hand_advert_parameters_type':
            await advert_parameters.advert_parameters__choose_state\
                .AdvertParametersChooseCarState().callback_handler(callback, state)

        case 'choose_specific_advert_parameter_value':
            await advert_parameters.advert_parameters__second_hand_state_handlers.choose_parameter_type\
                .ChooseSecondHandAdvertParametersType().callback_handler(callback, state)
