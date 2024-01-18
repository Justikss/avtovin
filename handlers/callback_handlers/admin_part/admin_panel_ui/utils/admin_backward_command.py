import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.choose_advertisement_action import \
    choose_advertisement_action
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.review_inputted_data import \
    request_review_mailing_data
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.choose_mailing_action import \
    ChooseMailingAction
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.mailing_storage.choose_specific_type import \
    request_choose_mailing_type
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.choose_statistic_type import \
    ChooseStatisticTypeHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.custom_params.choose_param_handler import \
    ChooseParamToDemandStatsHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.setting_process.choose_period import \
    CustomParamsChoosePeriod
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.setting_process.calculate_method import \
    CalculateDemandMethodHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.setting_process.output_method import \
    StatisticsOutputMethodHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__choose_state import \
    AdvertParametersChooseCarState
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.new_car_state_parameters_handler import \
    NewCarStateParameters
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.add_new_value_advert_parameter.add_new_value_advert_parameter import \
    AddNewValueAdvertParameter
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters import \
    OutputSpecificAdvertParameters
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.choose_actions_on_exists_parameter import \
    ChooseActionOnAdvertParameterHandler
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
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.choose_type import ChooseContactsTypeHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.output.list import ContactListHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.output.specific import OutputSpecificContactHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.edit_tariff.edit_tariff_handler import \
    edit_tariff_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_tariff_data import process_tariff_cost, \
    process_write_tariff_feedbacks_residual, process_write_tariff_cost
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.output_specific_tariff import \
    output_specific_tariff_for_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.output_tariff_list import \
    output_tariffs_for_admin
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.tariff_for_seller.checkout_tariff_by_admin import \
    checkout_seller_tariff_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.tariff_for_seller.choose_tariff_for_seller import \
    checkout_tariff_for_seller_by_admin_handler, choose_tariff_for_seller_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_category.choose_seller_category import \
    choose_seller_category_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_category.choose_users_category import \
    choose_user_category_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_buyer import \
    output_buyer_profile
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_seller import \
    output_specific_seller_profile_handler

from handlers.callback_handlers.buy_part.language_callback_handler import set_language
from handlers.utils.delete_message import delete_message
from handlers.utils.message_answer_without_callback import send_message_answer
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog import advert_parameters


async def admin_backward_command_handler(callback: CallbackQuery, state: FSMContext):
    input_reason_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.user_ban.start_ban_process_input_reason')
    choose_specific_person_by_admin_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person')
    backward_mode = callback.data.split(':')[-1]

    handler_class = None
    current_state = str(await state.get_state())
    memory_storage = await state.get_data()

    ic(backward_mode)
    ic(memory_storage.get('params_type_flag') == 'new')
    match backward_mode:
        case 'start_delete_ts_contact' | 'confirmation_rewrite_ts' | 'start_rewrite_ts_contact':
            await OutputSpecificContactHandler().callback_handler(callback, state)
        case 'review_contacts_list' | 'to_type_contacts':
            await ChooseContactsTypeHandler().callback_handler(callback, state)
        case 'start_add_new_contact' | 'confirmation_add_new_ts' | 'review_profile':
            await ContactListHandler().callback_handler(callback, state)

        case 'choose_custom_params':
            await choose_custom_params_stats_backwarder(callback, state, memory_storage, current_state)
        case 'top_ten_display':
            await CustomParamsChoosePeriod().callback_handler(callback, state)
        case 'custom_params_period':
            await CalculateDemandMethodHandler().callback_handler(callback, state)

        case 'method_of_calculate':
            await StatisticsOutputMethodHandler().callback_handler(callback, state)

        case 'check_bot_statistic_values' | 'to_statistic_panel' | 'statistics_output_method':
            await ChooseStatisticTypeHandler().callback_handler(callback, state)

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

        case 'tariff_for_seller_review':
            await choose_tariff_for_seller_by_admin_handler(callback, state)

        case 'choose_tariff_for_seller' | 'reset_seller_tariff':
            await checkout_seller_tariff_by_admin_handler(callback, state)

        case 'tariff_to_seller_pre_confirm_moment':
            await checkout_tariff_for_seller_by_admin_handler(callback, state)

        case 'final_confirm_block_user':
            await input_reason_module.input_ban_reason_handler(callback, state)

        case 'input_tariff_cost' | 'input_tariff_feedbacks' | 'input_tariff_duration_time' | 'input_tariff_name' \
            if memory_storage.get('edit_tariff_mode'):
            await edit_tariff_by_admin_handler(callback, state)

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
                await ChooseMailingAction().callback_handler(callback, state)
            else:
                await request_review_mailing_data(callback, state)

        case 'choose_mailing_action':
            await choose_advertisement_action(callback, state)

        case 'choose_review_mailing_type':
            await ChooseMailingAction().callback_handler(callback, state)

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
            admin_pagination_module = importlib.import_module(
                'handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_pagination')

            if await admin_pagination_module.AdminPaginationOutput.output_page(callback, state, None) is False:
                Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
                await send_message_answer(callback, Lexicon_module.catalog_captions['inactive_advert_or_seller'])
                if await choose_review_catalog_brand_admin_handler(callback, state) is False:
                    await choose_review_catalog_type_admin_handler(callback, state)

        case 'catalog_review_close_action_confirmation':
            await input_reason_to_close_advert_admin_handler(callback, state, False)

        case 'input_reason_to_close_advert':
            await choose_specific_advert_action_admin_handler(callback, state)

        case 'choose_second_hand_advert_parameters_type' | 'go_to_choose_params_state':
            await advert_parameters.advert_parameters__choose_state\
                .AdvertParametersChooseCarState().callback_handler(callback, state)

        case 'choose_specific_advert_parameter_value' | 'await_input_new_parameter_value' \
            if memory_storage.get('params_type_flag') == 'new' and memory_storage.get('add_new_branch_status'):
            await backward_in_advert_parameters_interface(current_state, callback, state)

        case 'choose_specific_advert_parameter_value' | 'review_params_branch' | 'review_params_branch_to_load' | 'confirmation_add_value_process':
            await backward_in_advert_parameters_interface(current_state, callback, state)

        case 'await_input_new_parameter_value' | 'confirmation_add_new_parameter_value_cancel' | 'choose_action_on_specific_adv_parameter':
            match backward_mode:
                case 'confirmation_add_new_parameter_value_cancel':
                    if memory_storage.get('admin_incorrect_flag'):
                        await delete_message(callback, memory_storage.get('last_admin_answer'))
                    # if memory_storage.get('params_type_flag') == 'new':
                    #     return await backward_in_advert_parameters_interface(current_state, callback, state)
            ic()
            await advert_parameters.parameters_ouptut.output_specific_parameters\
                .OutputSpecificAdvertParameters().callback_handler(callback, state)#

        case 'confirmation_add_new_parameter_value_rewrite':
            await AddNewValueAdvertParameter().callback_handler(callback, state)

        case 'confirmation_delete_advert_param' | 'rewrite_exists_advert_param' | 'start_rewrite_exists_parameter_value':
            if memory_storage.get('params_type_flag') == 'new':
                await advert_parameters.parameters_ouptut.output_specific_parameters \
                    .OutputSpecificAdvertParameters().callback_handler(callback, state)  #
            else:
                await ChooseActionOnAdvertParameterHandler().callback_handler(callback, state)



async def backward_in_advert_parameters_interface(current_state, callback, state):
    current_parameters_to_output = None
    next_parameters_to_output = None
    delete_mode = False
    ic(current_state)
    parameters = ['state', 'engine', 'brand', 'model', 'complectation', 'color']
    match current_state:
        case 'AdminAdvertParametersStates.NewStateStates:chosen_state':
            await AdvertParametersChooseCarState().callback_handler(callback, state)
        case 'AdminAdvertParametersStates.NewStateStates:parameters_branch_review' | \
            'AdminAdvertParametersStates.NewStateStates:confirmation_new_params_branch_to_load' | \
            'AdminAdvertParametersStates.NewStateStates:await_input_new_car_photos':

            if current_state in ('AdminAdvertParametersStates.NewStateStates:parameters_branch_review',
                                 'AdminAdvertParametersStates.NewStateStates:confirmation_new_params_branch_to_load'):
                delete_mode = True

            current_parameters_to_output = 'color'
            next_parameters_to_output = 'complectation'
        case 'AdminAdvertParametersStates:start_add_value_process' | 'AdminAdvertParametersStates:confirmation_add_value_process':
            add_new_branch_status = await OutputSpecificAdvertParameters().check_state_on_add_new_branch_status(state)
            if add_new_branch_status:
                pass
            memory_storage = await state.get_data()
            ic(add_new_branch_status)
            next_parameters_to_output = memory_storage.get('next_params_output')
            ic(current_parameters_to_output)
            current_parameters_to_output = parameters[parameters.index(next_parameters_to_output)-1]
            ic(next_parameters_to_output)

        case _:#
            ic()
            if 'NewStateStates' in current_state:
                param_name = current_state.split('_')[-1]
                ic(param_name)
                if param_name == 'state':
                    return await AdvertParametersChooseCarState().callback_handler(callback, state)

                if param_name in parameters:
                    current_parameters_to_output = param_name
                    next_parameters_to_output = parameters[parameters.index(param_name)+1]
            else:
                await advert_parameters.advert_parameters__second_hand_state_handlers.choose_parameter_type \
                .ChooseSecondHandAdvertParametersType().callback_handler(callback, state)

    ic(next_parameters_to_output)
    if next_parameters_to_output:
        memory_storage = await state.get_data()
        ic(current_parameters_to_output)
        if current_parameters_to_output == 'review':
            current_parameters_to_output = 'color'
        selected_parameters = memory_storage.get('selected_parameters')
        ic(selected_parameters, current_parameters_to_output)
        if current_parameters_to_output in selected_parameters.keys():
            selected_parameters.pop(current_parameters_to_output)
        await state.update_data(selected_parameters=selected_parameters)

        await NewCarStateParameters().set_state_by_param(state, current_parameters_to_output)
        await state.update_data(next_params_output=current_parameters_to_output)
        ic()
        await OutputSpecificAdvertParameters().callback_handler(callback, state, delete_mode=delete_mode)#


async def choose_custom_params_stats_backwarder(callback: CallbackQuery, state: FSMContext, memory_storage=None, current_state=None):
    if not memory_storage:
        memory_storage = await state.get_data()
    if not current_state:
        current_state = str(await state.get_state())

    chosen_demand_params = memory_storage.get('chosen_demand_params')
    out_flag = False
    if chosen_demand_params:
        chosen_demand_params_keys = chosen_demand_params.keys()
        ic(chosen_demand_params_keys)
        all_params_to_choose = ['engine', 'brand', 'model', 'complectation', 'color']
        for param_type in reversed(all_params_to_choose):
            if param_type in chosen_demand_params_keys:
                ic()
                ic(chosen_demand_params)
                chosen_demand_params.pop(param_type)
                ic(chosen_demand_params)
                await state.update_data(chosen_demand_params=chosen_demand_params)

                if current_state == 'StatisticsStates.CustomParams:review_process':
                    await state.update_data(media_group_for_inline_pg=None)
                break

        await ChooseParamToDemandStatsHandler().callback_handler(callback, state)
    else:
    #     out_flag = True
    #
    # if out_flag:
    #     # await state.update_data(chosen_demand_params=None)
        await CustomParamsChoosePeriod().callback_handler(callback, state)