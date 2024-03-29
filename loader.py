import asyncio
import importlib

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter, and_f, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.types import Message, CallbackQuery

from icecream import ic

from database.data_requests.tariff_requests import TarifRequester
from database.db_connect import create_tables
from handlers.callback_handlers.admin_part import admin_panel_ui
from handlers.callback_handlers.admin_part.admin_panel_ui import user_actions, tariff_actions, catalog
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions import mailing
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.choose_statistic_type import \
    ChooseStatisticTypeHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.custom_params.choose_param_handler import \
    ChooseParamToDemandStatsHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.custom_params.output_param_branches import \
    OutputStatisticAdvertParamsHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.setting_process.calculate_method import \
    CalculateDemandMethodHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.setting_process.choose_period import \
    CustomParamsChoosePeriod
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.setting_process.output_method import \
    StatisticsOutputMethodHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.setting_process.output_type_handler import \
    DemandOutputSplitterHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.top_ten_display import \
    TopTenByDemandDisplayHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.general_statistics.general_statistic import \
    GeneralBotStatisticHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.new_car_state_parameters_handler import \
    NewCarStateParameters

from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.add_new_branch_confirm.confirm_add_new_branch_handler import \
    ConfirmLoadNewParamsBranchHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.add_new_value_advert_parameter.input_media_group_to_advert.input_media import \
    InputCarPhotosToSetParametersBranchHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_deletion.confirm_deletion import \
    ConfirmDeleteExistsAdvertParameter
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_deletion.start_deletion import \
    ActionOfDeletionExistsAdvertParameter
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_rewriting.confirm import \
    ConfirmRewriteExistsAdvertParameterHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_rewriting.confirmation import \
    ConfirmationRewriteExistsAdvertParameterHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_rewriting.start import \
    RewriteExistsAdvertParameterHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.change_state.confirm import \
    ConfirmChangeStateOnExistsBranchHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.change_state.start import \
    ChangeStateOnExistsBranchHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.choose_actions_on_exists_parameter import \
    ChooseActionOnAdvertParameterHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.choose_car_state import \
    ChooseStateAddNewParamsHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.actions.add.confirm import \
    ConfirmAddNewContactHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.actions.add.confirmation import \
    ConfirmationAddNewContactHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.actions.add.start import StartAddNewContactHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.actions.delete.confirm import \
    ConfirmDeleteTSContactHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.actions.delete.confirmation import \
    ConfirmationDeleteTSContactHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.actions.rewrite.confirm import \
    ConfirmRewriteExistsTSContact
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.actions.rewrite.confirmation import \
    ConfirmationRewriteExistsTSContact
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.actions.rewrite.start import \
    StartRewriteExistsTSContact
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.choose_type import ChooseContactsTypeHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.output.list import ContactListHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.contacts.output.specific import OutputSpecificContactHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user import tariff_for_seller, user_ban
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.user_unban.confirm import \
    confirm_unblock_user
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.user_unban.confirmation import \
    user_unban_confirmation
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_category.choose_block_user_category import \
    choose_user_block_status
from handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_pagination import AdminPaginationOutput
from handlers.callback_handlers.buy_part.buyer_offers_branch.offers_handler import buyer_offers_callback_handler

from handlers.callback_handlers.buy_part.buyer_offers_branch.show_requests import output_buyer_offers
from handlers.callback_handlers.hybrid_part.utils.media_group_structurier_collector import handle_media
from handlers.callback_handlers.sell_part.commodity_requests.backward_command_load_config import backward_in_boot_car
from handlers.callback_handlers.sell_part.commodity_requests.rewrite_price_by_seller import \
    rewrite_price_by_seller_handler, get_input_to_rewrite_price_by_seller_handler
from handlers.custom_filters.admin_filters.admin_status_controller import AdminStatusController
from handlers.custom_filters.admin_filters.block_user_reason_input import ControlInputUserBlockReason
from handlers.custom_filters.admin_filters.catalog_filters.input_value_advert_parameter_filter import \
    AdvertParameterValueFilter
from handlers.custom_filters.admin_filters.mailing_filters.datetime_input_filter import DateTimeFilter
from handlers.custom_filters.admin_filters.digit_input_filter import DigitFilter
from handlers.custom_filters.admin_filters.mailing_filters.input_media_filter import MediaFilter
from handlers.custom_filters.admin_filters.mailing_filters.mailing_text_filter import MailingTextFilter
from handlers.custom_filters.admin_filters.red_admin_status import RedAdminStatus
from handlers.custom_filters.admin_filters.search_advert_by_id_filter import InputAdvertIdFilter
from handlers.custom_filters.admin_filters.tariff_duration_time_filter import TimeDurationFilter
from handlers.custom_filters.admin_filters.ts_contacts_filters.input_link_filter import InputTSLinkFilter
from handlers.custom_filters.admin_filters.unique_tariff_name import UniqueTariffNameFilter
from handlers.custom_filters.developer import CheckOnDeveloper
from handlers.custom_filters.pass_on_dealership_address import GetDealershipAddress
from handlers.custom_filters.throttling import ThrottlingFilter
from handlers.custom_filters.user_not_is_banned import UserBlockStatusController
from handlers.custom_handlers.admin_administrating.admin_list import AdminListHandler
from handlers.custom_handlers.admin_administrating.del_admin import DelAdminHandler
from handlers.custom_handlers.admin_administrating.del_red_admin import DelRedAdminHandler
from handlers.custom_handlers.admin_administrating.help import AdminHelpHandler
from handlers.custom_handlers.admin_administrating.set_admin import SetAdminHandler
from handlers.custom_handlers.admin_administrating.set_red_admin import SetRedAdminHandler
from handlers.custom_handlers.admin_administrating.unban_person import UnbanPersonAdminHandler
from handlers.custom_handlers.developer_handlers.add_new_db_columns import add_db_columns
from handlers.custom_handlers.developer_handlers.clear_cached_configs import del_cached_configs
from handlers.custom_handlers.developer_handlers.delete_all_messages import delete_all_messages_developer_handler
from handlers.custom_handlers.developer_handlers.stop_develop_moment import close_develop_moment_handler
from handlers.default_handlers.drop_table import drop_table_handler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.empty_field_handler import EmptyFieldCarpoolingHandler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.price_filtration.choose_diapason_side import \
    ChooseCarPriceFilterHandler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.price_filtration.close_review_window import \
    CloseWindowCarPriceFilterHandler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.price_filtration.input_edge_cost.confirm import \
    ConfirmInputtedCarPriceFilterValueInputHandler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.price_filtration.input_edge_cost.confirmation import \
    ConfirmationCarPriceFilterInputHandler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.price_filtration.input_edge_cost.start import \
    StartInputCarPriceFilterStartInputHandler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.price_filtration.input_edge_cost.utils.reset_current_range_side import \
    ResetCurrentRangeSideForBuyer
from handlers.state_handlers.seller_states_handler.load_new_car.cancel_boot_process_handler import \
    cancel_boot_process_callback_handler
from handlers.utils.inline_buttons_pagination_heart import CachedRequestsView
from handlers.callback_handlers.sell_part.commodity_requests.delete_car_request import DeleteCarRequest
from handlers.callback_handlers.sell_part.commodity_requests.pagination_handlers import SellerRequestPaginationHandlers
from handlers.callback_handlers.sell_part.commodity_requests.sellers_feedbacks.delete_feedback import DeleteFeedback
from handlers.callback_handlers.sell_part.commodity_requests.sellers_feedbacks.my_feedbacks_button import \
    CheckFeedbacksHandler
from handlers.custom_handlers.lost_photos_handler import lost_photos_handler

from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_cars_pagination_system.pagination_system_controller import \
    BuyerPaginationVector
from handlers.state_handlers.seller_states_handler.load_new_car.edit_boot_data import edit_boot_car_data_handler
from handlers.utils.plugs.page_counter_plug import page_conter_plug
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from states.admin_part_states.catalog_states.catalog_review_states import AdminCarCatalogReviewStates, \
    AdminCarCatalogSearchByIdStates
from states.admin_part_states.mailing.mailing_setup_states import MailingStates
from states.admin_part_states.statistics_states import StatisticsStates
from states.admin_part_states.tariffs_branch_states import TariffAdminBranchStates, TariffEditState
from states.admin_part_states.tech_support_states import TechSupportStates
from states.admin_part_states.users_review_states import SellerReviewStates, BuyerReviewStates
from states.buyer_offers_states import CheckNonConfirmRequestsStates, CheckActiveOffersStates, \
    CheckRecommendationsStates
from states.cost_filter_in_buy_search import BuyerSearchCostFilterStates
from states.input_rewrited_price_by_seller import RewritePriceBySellerStates
from states.requests_by_seller import SellerRequestsState
from states.seller_feedbacks_states import SellerFeedbacks
from utils.asyncio_tasks.invalid_tariffs_deleter import schedule_tariff_deletion
from utils.asyncio_tasks.old_messages_cleaner import check_on_old_messages
from utils.get_currency_sum_usd import fetch_currency_rate
from utils.mailing_heart.mailing_service import mailing_service
from utils.middleware.update_spam_defender.middleware import UpdateThrottlingMiddleware
from utils.user_notification import delete_notification_for_seller, try_delete_notification
from handlers.callback_handlers.buy_part import FAQ_tech_support, backward_callback_handler, callback_handler_backward_in_carpooling, callback_handler_start_buy, \
    confirm_search_config, language_callback_handler
from handlers.callback_handlers.buy_part.buyer_offers_branch import show_requests
from handlers.custom_filters import correct_name, correct_number, pass_on_dealership_address, price_is_digit, message_is_photo
from handlers.default_handlers import start
from handlers.state_handlers import buyer_registration_handlers
from handlers.state_handlers.buyer_registration_handlers import BuyerRegistationStates
from handlers.state_handlers.choose_car_for_buy import hybrid_handlers, second_hand_car_handlers
from states.hybrid_choose_states import HybridChooseStates
from states.second_hand_choose_states import SecondHandChooseStates
from states.load_commodity_states import LoadCommodityStates
from states.tariffs_to_seller import ChoiceTariffForSellerStates
from states.seller_registration_states import HybridSellerRegistrationStates, CarDealerShipRegistrationStates
from handlers.callback_handlers.sell_part import start_sell_button_handler, start_seller_registration_callback_handlers, \
    commodity_requests
from handlers.callback_handlers.admin_part import accept_registration_request_button
from handlers.callback_handlers import sell_part
from handlers.state_handlers.seller_states_handler.seller_registration import seller_registration_handlers, \
    await_confirm_from_admin, check_your_registration_config
from handlers.state_handlers.seller_states_handler import load_new_car, seller_profile_branch
from handlers.callback_handlers.hybrid_part import return_main_menu
from handlers.callback_handlers.hybrid_part.faq import seller_faq, buyer_faq, faq
from handlers.callback_handlers.hybrid_part.utils.media_group_collector import collect_and_send_mediagroup


redis = None
bot = None

# Определение контекстной переменной для языка

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)
# ic.disable()
dp = Dispatcher(storage=storage)
profiler = None


async def start_bot():
    global redis, edit_last_message, bot, dp, redis, storage
    config_module = importlib.import_module('config_data.config')

    bot = Bot(token=config_module.BOT_TOKEN, parse_mode='HTML')
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)

    await create_tables()
    await TarifRequester.create_tarifs()
    await mailing_service.schedule_mailing(bot)


    asyncio.create_task(check_on_old_messages(bot))
    asyncio.create_task(fetch_currency_rate())
    asyncio.create_task(schedule_tariff_deletion(bot))
    asyncio.create_task(GetDealershipAddress.process_queue())

    dp.update.outer_middleware(UpdateThrottlingMiddleware())

    # @dp.callback_query(F.data == 'seller_requests')
    async def totts(callback: CallbackQuery, state: FSMContext):
        from handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs import \
            output_load_config_for_seller
        from database.data_requests.car_configurations_requests import CarConfigs
        co = await CarConfigs.custom_action('Elpos', 'get_by_name', model_id='also')
        b = await CarConfigs.custom_action('brand', 'get_by_name', model_id='also')
        m = await CarConfigs.custom_action('model', 'get_by_name', model_id='slos')
        await state.set_data({'boot_car_states_cache': ['LoadCommodityStates:input_to_load_engine_type',
                                               'LoadCommodityStates:input_to_load_brand',
                                               'LoadCommodityStates:input_to_load_model',
                                               'LoadCommodityStates:input_to_load_complectation',
                                               'LoadCommodityStates:input_to_load_color',
                                               'LoadCommodityStates:input_to_load_price',
                                               'LoadCommodityStates:input_to_load_photo'],
                     'brand_for_load': b.id,
                     'color_for_load': 6,
                     'complectation_for_load': f'[236, {co.id}]',
                     'dollar_price': None,
                     'dynamic_buttons': 2,
                     'engine_for_load': 1,
                     'head_valute': 'sum',
                     'incorrect_flag': False,
                     'last_buttons': {'boot_car_backward': '◂ Назад ▸',
                                      'cancel_boot_new_commodity': 'Отмена'},
                     'message_text': '<b>Предпочитаемый цвет:</b>',
                     'model_for_load': m.id,
                     'state_for_load': 1,
                     'sum_price': 56657657,
                     'width': 2})
        await state.set_state(LoadCommodityStates.input_to_load_photo)
        await output_load_config_for_seller(callback, state)

    dp.message.register(handle_media, or_f(F.photo, F.video, F.audio, F.document),
                        StateFilter(MailingStates.entering_date_time))
    dp.message.register(collect_and_send_mediagroup,
                        F.photo, F.photo[-1].file_id.as_("photo_id"), F.photo[-1].file_unique_id.as_('unique_id'),
                        F.photo[-1].width.as_('photo_width'), F.photo[-1].height.as_('photo_height'))

    dp.message.register(drop_table_handler,
                        Command(commands=['dt', 'dtc']), CheckOnDeveloper())
    dp.message.register(delete_all_messages_developer_handler,
                        Command(commands=["startdev"], ignore_case=True), CheckOnDeveloper())
    dp.message.register(close_develop_moment_handler, Command(commands=['stopdev'], ignore_case=True),
                        CheckOnDeveloper())

    dp.message.register(del_cached_configs, Command(commands=['delres'], ignore_case=True), CheckOnDeveloper())
    dp.message.register(add_db_columns, Command(commands=["add_cols"], ignore_case=True), CheckOnDeveloper())

    '''обработка Сообщений'''

    dp.message.register(start.bot_start,
                        Command(commands=["start"], ignore_case=True), ThrottlingFilter())


    '''Состояния регистрации покупателя'''
    dp.callback_query.register(buyer_registration_handlers.input_full_name,
                               StateFilter(BuyerRegistationStates.input_full_name))
    dp.message.register(buyer_registration_handlers.input_phone_number,
                        StateFilter(BuyerRegistationStates.input_phone_number), ThrottlingFilter(),
                        correct_name.CheckInputName())
    dp.message.register(buyer_registration_handlers.finish_check_phone_number,
                        StateFilter(BuyerRegistationStates.finish_check_phone_number), ThrottlingFilter(),
                        correct_number.CheckInputNumber())
    '''Состояния регистрации продавцов'''
    dp.callback_query.register(await_confirm_from_admin.seller_confirm_registration,
                              F.data == 'confirm_registration_from_seller')

    dp.callback_query.register(start_seller_registration_callback_handlers.seller_type_identifier,
                                    F.data.in_(('i_am_private_person', 'i_am_car_dealership')))

    dp.message.register(seller_registration_handlers.hybrid_input_seller_number,
                        and_f(StateFilter(HybridSellerRegistrationStates.input_number), ThrottlingFilter(),
                              correct_name.CheckInputName()))

    dp.message.register(seller_registration_handlers.dealership_input_address,
                        and_f(StateFilter(CarDealerShipRegistrationStates.input_dealship_name), ThrottlingFilter(),
                              correct_number.CheckInputNumber()))



    dp.callback_query.register(seller_registration_handlers.hybrid_input_seller_number,
                        and_f(StateFilter(HybridSellerRegistrationStates.check_input_data),
                        F.data == 'rewrite_seller_number'))

    dp.callback_query.register(seller_registration_handlers.input_seller_name,
                              and_f(StateFilter(HybridSellerRegistrationStates.check_input_data),
                              F.data == 'rewrite_seller_name'))

    dp.callback_query.register(seller_registration_handlers.dealership_input_address,
                              and_f(StateFilter(HybridSellerRegistrationStates.check_input_data),
                               F.data == 'rewrite_dealership_address'))

    dp.message.register(check_your_registration_config.check_your_config,
                        and_f(StateFilter(HybridSellerRegistrationStates.check_input_data), ThrottlingFilter(),
                        pass_on_dealership_address.GetDealershipAddress()))

    '''Пагинация клавиатуры'''
    dp.callback_query.register(CachedRequestsView.inline_buttons_pagination_vector_handler,
                               F.data.in_(('inline_buttons_pagination:-', 'inline_buttons_pagination:+')))

    dp.callback_query.register(AdminPaginationOutput.admin_pagination_vector,
                               lambda callback: callback.data.startswith('admin_pagination'))

    '''Пагинация неподтверждённых заявок'''
    dp.callback_query.register(output_buyer_offers,
                               or_f(StateFilter(CheckNonConfirmRequestsStates.await_input_brand),
                                    StateFilter(CheckActiveOffersStates.await_input_brand),
                                    StateFilter(CheckRecommendationsStates.await_input_brand)),
                               lambda callback: callback.data.startswith('load_brand_'))

    '''delete request'''
    dp.callback_query.register(DeleteCarRequest.delete_car_handler, F.data == 'withdrawn')

    dp.callback_query.register(DeleteCarRequest.accept_delete_car_and_backward_from_delete_menu_handler, F.data.in_(
        ("i'm_sure_delete", 'backward_from_delete_car_menu', 'backward_from_delete_feedback_menu')))

    '''обработка Коллбэков'''
    dp.callback_query.register(FAQ_tech_support.tech_support_callback_handler, F.data == 'support')
    dp.callback_query.register(FAQ_tech_support.write_to_support_callback_handler, F.data == 'write_to_support')
    dp.callback_query.register(FAQ_tech_support.call_to_support_callback_handler, F.data == 'call_to_support')
    '''buyer'''
    dp.callback_query.register(buyer_offers_callback_handler, F.data == 'buyer_requests')
    dp.callback_query.register(callback_handler_backward_in_carpooling.backward_in_carpooling_handler,
                               F.data == 'backward_in_carpooling')
    dp.callback_query.register(language_callback_handler.set_language,
                               F.data.in_(('language_uz', 'language_ru')))
    dp.callback_query.register(callback_handler_start_buy.start_buy,
                               F.data == 'start_buy')
    ic()
    dp.callback_query.register(backward_callback_handler.backward_button_handler,
                               lambda callback: callback.data.startswith('backward'))
    dp.callback_query.register(hybrid_handlers.search_auto_callback_handler,
                               F.data == 'car_search', UserBlockStatusController())
    dp.callback_query.register(confirm_search_config.confirm_settings_handler,
                               lambda callback: callback.data.startswith('confirm_buy_settings:'), UserBlockStatusController())

    dp.callback_query.register(show_requests.buyer_get_requests__chose_brand, F.data.in_(
        ('buyer_cached_offers', 'buyer_active_offers', 'buyers_recommended_offers', 'buyers_recommended_offers',
         'return_to_choose_requests_brand')
    ), UserBlockStatusController())

    '''Seller'''
    dp.callback_query.register(delete_notification_for_seller, lambda callback: callback.data.startswith('close_seller_notification:'))

    dp.callback_query.register(try_delete_notification, or_f(
        lambda callback: callback.data.startswith('close_seller_notification_by_redis'),
        lambda callback: callback.data.startswith('close_ban_notification:'),
        lambda callback: callback.data.startswith('close_unblock_notification:')

    ))

    dp.callback_query.register(start_sell_button_handler.start_sell_callback_handler,
                              or_f(F.data == 'start_sell', F.data == 'return_to_start_seller_registration'))

    dp.callback_query.register(accept_registration_request_button.accept_registraiton,
                               lambda callback: callback.data.startswith('confirm_new_seller_registration_from'))

    dp.callback_query.register(faq.FAQ_callback_handler, F.data == 'faq')
    dp.callback_query.register(seller_faq.seller_faq, F.data == 'seller_faq')
    dp.callback_query.register(buyer_faq.buyer_faq, F.data == 'buyer_faq')

    dp.callback_query.register(sell_part.commodity_requests.commodity_requests_handler.commodity_reqests_by_seller,
                        F.data == 'seller_requests')

    dp.callback_query.register(commodity_requests.confirm_load_config_from_seller.confirm_load_config_from_seller,
                              F.data == 'confirm_load_config_from_seller', UserBlockStatusController())

    dp.callback_query.register(sell_part.checkout_seller_person_profile.output_seller_profile,
                              F.data == 'seller_pofile', UserBlockStatusController())

    sell_main_module = importlib.import_module('handlers.callback_handlers.sell_part.seller_main_menu')
    dp.callback_query.register(sell_main_module.seller_main_menu,
                               F.data == 'seller_main_menu')

    '''seller"s requests'''
    dp.callback_query.register(
        sell_part.commodity_requests.my_requests_handler.seller_requests_callback_handler,
        F.data == 'my_sell_requests')

    dp.callback_query.register(
        sell_part.commodity_requests.output_sellers_requests.output_sellers_requests_by_car_brand_handler, StateFilter(SellerRequestsState.await_input_brand),
        lambda callback: callback.data.startswith('seller_requests_brand:'))

    dp.callback_query.register(SellerRequestPaginationHandlers.seller_request_pagination_vectors,
                               F.data.in_(('seller_requests_pagination_left', 'seller_requests_pagination_right')))

    dp.callback_query.register(rewrite_price_by_seller_handler, F.data == 'rewrite_price_by_seller')
    dp.message.register(get_input_to_rewrite_price_by_seller_handler, StateFilter(RewritePriceBySellerStates.await_input),
                        ThrottlingFilter(), price_is_digit.PriceIsDigit())
    '''seller"s feedbacks'''

    dp.callback_query.register(CheckFeedbacksHandler.my_feedbacks_callback_handler, lambda callback: callback.data.startswith('my_sell_feedbacks'))

    dp.callback_query.register(CheckFeedbacksHandler.check_feedbacks_handler, and_f(StateFilter(SellerFeedbacks.choose_feedbacks_state),
                               F.data.in_(('new_feedbacks', 'viewed_feedbacks')), UserBlockStatusController()))

    dp.callback_query.register(DeleteFeedback.delete_feedback_handler, F.data == "i'm_sure_delete_feedback")

    dp.callback_query.register(DeleteFeedback.did_you_sure_to_delete_feedback_ask, F.data == 'deal_fell_through')

    '''Оформление тарифа продавца'''
    dp.callback_query.register(seller_profile_branch.tariff_extension.output_affordable_tariffs_handler, F.data == 'tariff_extension')
    dp.callback_query.register(seller_profile_branch.selected_tariff_preview.tariff_preview_handler,
                              and_f(StateFilter(ChoiceTariffForSellerStates.choose_tariff), lambda callback: callback.data.startswith('select_tariff:')))
    dp.callback_query.register(seller_profile_branch.choose_payment.choice_payments_handler,
                              and_f(StateFilter(ChoiceTariffForSellerStates.preview_tariff),
                                    F.data == 'start_choose_payment_method', UserBlockStatusController()))

    dp.callback_query.register(seller_profile_branch.payments.payment_invoice_sender.send_invoice_offer,
                              and_f(StateFilter(ChoiceTariffForSellerStates.choose_payment_method),
                                     lambda callback: callback.data.startswith('run_tariff_payment:')))

    '''hybrid'''

    dp.callback_query.register(return_main_menu.return_main_menu_callback_handler,
                               F.data == 'return_main_menu')

    '''admin'''
    dp.callback_query.register(admin_panel_ui.utils.admin_backward_command.admin_backward_command_handler,
                               lambda callback: callback.data.startswith('admin_backward'), AdminStatusController())

    dp.callback_query.register(admin_panel_ui.start_admin_panel_window.start_admin_menu, F.data == 'admin_panel_button',
                               AdminStatusController())

    dp.callback_query.register(choose_user_block_status,
                               F.data.in_(('admin_button_users',
                                           'check_banned_persons')))


    dp.callback_query.register(tariff_actions.output_tariff_list.output_tariffs_for_admin,
                               F.data == 'admin_button_tariffs', AdminStatusController())

    dp.callback_query.register(admin_panel_ui.advertisement_actions.choose_advertisement_action.choose_advertisement_action,
                               F.data == 'admin_button_advert')

    dp.callback_query.register(catalog.choose_catalog_action.choose_catalog_action_admin_handler,
                               F.data == 'admin_button_catalog')

    dp.callback_query.register(ChooseStatisticTypeHandler().callback_handler,
                               F.data == 'admin_button_bot_statistics')

    '''tech-support contacts'''
    dp.callback_query.register(ChooseContactsTypeHandler().callback_handler,
                               F.data == 'admin_button_contacts'),
    dp.callback_query.register(ContactListHandler().callback_handler,
                               lambda callback: callback.data.startswith('ts_contact_type:'))
    dp.callback_query.register(OutputSpecificContactHandler().callback_handler,
                               lambda callback: callback.data.startswith('review_ts_contact:'),
                               StateFilter(TechSupportStates.review))

    dp.callback_query.register(StartAddNewContactHandler().callback_handler,
                               StateFilter(TechSupportStates.review),
                               F.data.in_(('add_ts_contact', 'rewrite_ts_contact_link')))
    dp.message.register(ConfirmationAddNewContactHandler(filters=InputTSLinkFilter()).message_handler,
                        StateFilter(TechSupportStates.add_new), ThrottlingFilter())
    dp.callback_query.register(ConfirmAddNewContactHandler().callback_handler,
                               F.data == 'confirm_add_ts_contact',
                               StateFilter(TechSupportStates.review),
                               AdminStatusController())

    dp.callback_query.register(ConfirmationDeleteTSContactHandler().callback_handler,
                               F.data == 'delete_ts_contact',
                               StateFilter(TechSupportStates.review))
    dp.callback_query.register(ConfirmDeleteTSContactHandler().callback_handler,
                               F.data == 'confirm_delete_contact',
                               StateFilter(TechSupportStates.delete_exists),
                               AdminStatusController())

    dp.callback_query.register(StartRewriteExistsTSContact().callback_handler,
                               F.data.in_(('edit_ts_contact', 'rewrite_rewriting_ts_contact')),
                               StateFilter(TechSupportStates.review))
    dp.message.register(ConfirmationRewriteExistsTSContact(filters=InputTSLinkFilter()).message_handler,
                        StateFilter(TechSupportStates.rewrite_exists), ThrottlingFilter())
    dp.callback_query.register(ConfirmRewriteExistsTSContact().callback_handler,
                               F.data == 'confirm_rewrite_ts_contact',
                               StateFilter(TechSupportStates.review),
                               AdminStatusController())

    '''bot statistics'''
    dp.callback_query.register(GeneralBotStatisticHandler().callback_handler,
                               or_f(and_f(StateFilter(StatisticsStates.general_bot_statistic),
                               lambda callback: callback.data.startswith('select_bot_statistic_period')),
                                    F.data == 'general_statistics'),
                               AdminStatusController())

    dp.callback_query.register(StatisticsOutputMethodHandler().callback_handler,
                               F.data == 'demand_for_cars')
    dp.callback_query.register(CalculateDemandMethodHandler().callback_handler,
                               lambda callback: callback.data.startswith('output_method:'),
                               StateFilter(StatisticsStates.accept_demand_output_method))

    dp.callback_query.register(CustomParamsChoosePeriod().callback_handler,
                               lambda callback: callback.data.startswith('calculate_method:'),
                               StateFilter(StatisticsStates.accept_demand_calculate_method)
                               )
    dp.callback_query.register(DemandOutputSplitterHandler().callback_handler,
                               lambda callback: callback.data.startswith('select_bot_statistic_period:'),
                               StateFilter(StatisticsStates.choose_period)
                               )
    dp.callback_query.register(TopTenByDemandDisplayHandler().callback_handler,
                               lambda callback: callback.data.startswith('ttp:'),
                               StateFilter(StatisticsStates.display_top_ten),
                               AdminStatusController())

    dp.callback_query.register(ChooseParamToDemandStatsHandler().callback_handler,
                               or_f(and_f(
                                       StateFilter(StatisticsStates.choose_period),
                                       lambda callback: callback.data.startswith('select_bot_statistic_period:')),
                                   and_f(
                                       StateFilter(StatisticsStates.CustomParams.choose_params),
                                       lambda callback: callback.data.startswith('custom_demand_param:'),
                               StateFilter(StatisticsStates.CustomParams.choose_params)
                               )),
                               AdminStatusController())
    dp.callback_query.register(OutputStatisticAdvertParamsHandler().callback_handler,
                               StateFilter(StatisticsStates.CustomParams.choose_params),
                               F.data == 'output_current_demand_stats',
                               AdminStatusController()
                               )


    '''catalog_action'''
    dp.callback_query.register(
        catalog.car_catalog_review.search_advert_by_id.input_advert_id_for_search.input_advert_id_for_search_admin_handler,
        F.data == 'search_by_id')
    dp.message.register(
        catalog.car_catalog_review.search_advert_by_id.inputted_advert_id_to_search_handler.inputted_advert_id_for_search_admin_handler,
        StateFilter(AdminCarCatalogSearchByIdStates.await_input_for_admin), ThrottlingFilter(), InputAdvertIdFilter())

    dp.callback_query.register(catalog.car_catalog_review.catalog_review_choose_action.choose_review_catalog_type_admin_handler,
                               F.data == 'admin_catalog__car_catalog_review')
    dp.callback_query.register(
        catalog.car_catalog_review.output_choose.output_choose_brand_to_catalog_review.choose_review_catalog_brand_admin_handler,
   lambda callback: callback.data.startswith('car_catalog_review__'))
    dp.callback_query.register(
        catalog.car_catalog_review.output_choose.output_specific_advert.output_review_adverts_catalog_admin_handler,
    lambda callback: callback.data.startswith('admin_catalog_review_brand:'))

    dp.callback_query.register(
        catalog.car_catalog_review.catalog__specific_advert_actions.choose_specific_action.choose_specific_advert_action_admin_handler,
        F.data == 'admin_review_catalog_delete_advert')
    dp.callback_query.register(
        catalog.car_catalog_review.catalog__specific_advert_actions.catalog_review__input_action_reason.input_reason_to_close_advert_admin_handler,
        lambda callback: callback.data.startswith('catalog_action__')
    )
    ic()
    dp.message.register(
        catalog.car_catalog_review.catalog__specific_advert_actions.process_confirmation_current_action.confirmation_reason_to_close_advert_admin_handler,
        StateFilter(AdminCarCatalogReviewStates.await_input_reason_action), ThrottlingFilter(),
        ControlInputUserBlockReason()
    )
    dp.callback_query.register(
        catalog.car_catalog_review.catalog__specific_advert_actions.confirm_current_action.confirm_specific_advert_action_admin_handler,
        lambda callback: callback.data.startswith('catalog_review__confirm_'),
        AdminStatusController())

    '''admin_commands'''
    dp.message.register(DelAdminHandler(filters=RedAdminStatus()).message_handler,
                        Command(commands=['del'], ignore_case=True), ThrottlingFilter())
    dp.message.register(DelRedAdminHandler(filters=RedAdminStatus()).message_handler,
                        Command(commands=['rdel'], ignore_case=True), ThrottlingFilter())
    dp.message.register(SetAdminHandler(filters=RedAdminStatus()).message_handler,
                        Command(commands=['add'], ignore_case=True), ThrottlingFilter())
    dp.message.register(SetRedAdminHandler(filters=RedAdminStatus()).message_handler,
                        Command(commands=['radd'], ignore_case=True), ThrottlingFilter())
    dp.message.register(AdminListHandler(filters=AdminStatusController()).message_handler,
                        Command(commands=['alist'], ignore_case=True), ThrottlingFilter())
    dp.message.register(AdminHelpHandler(filters=AdminStatusController()).message_handler,
                        Command(commands=['ahelp'], ignore_case=True), ThrottlingFilter())
    dp.message.register(UnbanPersonAdminHandler(filters=AdminStatusController()).message_handler,
                        Command(commands=['unban'], ignore_case=True), ThrottlingFilter())

    '''advert_parameters'''
    dp.callback_query.register(catalog.advert_parameters.advert_parameters__choose_state\
                               .AdvertParametersChooseCarState().callback_handler,
                               F.data == 'admin_catalog__advert_parameters')

    dp.callback_query.register(
        catalog.advert_parameters.advert_parameters__second_hand_state_handlers.choose_parameter_type\
        .ChooseSecondHandAdvertParametersType().callback_handler,
       F.data == "advert_parameters_choose_state:2"
    )

    dp.callback_query.register(
        catalog.advert_parameters.parameters_ouptut.output_specific_parameters \
            .OutputSpecificAdvertParameters().callback_handler,
        lambda callback: '_choice_advert_parameters_type_' in callback.data,
        StateFilter(AdminAdvertParametersStates.review_process)
    )

    dp.callback_query.register(
        admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils\
            .add_new_value_advert_parameter.add_new_value_advert_parameter \
            .AddNewValueAdvertParameter().callback_handler,
        F.data == 'add_new_advert_parameter'
    )
    dp.message.register(
        admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils\
            .add_new_value_advert_parameter.input_confirmation \
            .AddNewValueOfAdvertParameterConfirmationMessageHandler(
            filters=AdvertParameterValueFilter()).message_handler,
        StateFilter(AdminAdvertParametersStates.start_add_value_process),
        ThrottlingFilter()
    )
    dp.callback_query.register(
        admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils\
            .add_new_value_advert_parameter.confirm_add_new_value_of_advert_parameter \
            .ConfirmAddNewValueOfAdvertParameter().callback_handler,
        F.data == 'confirm_action_add_new_parameter_value',
        StateFilter(AdminAdvertParametersStates.confirmation_add_value_process),
        AdminStatusController()
    ),
    dp.callback_query.register(
        ChooseActionOnAdvertParameterHandler().callback_handler,
        lambda callback: callback.data.startswith('advert_parameters_specific_value:')
    )

    dp.callback_query.register(
        ActionOfDeletionExistsAdvertParameter().callback_handler,
        F.data == 'delete_current_advert_parameter'
    )
    dp.callback_query.register(
        ConfirmDeleteExistsAdvertParameter().callback_handler,
        F.data == 'confirm_delete_advert_parameter',
        # StateFilter(AdminAdvertParametersStates.start_delete_action),
        AdminStatusController()
    )

    dp.callback_query.register(RewriteExistsAdvertParameterHandler().callback_handler,
                               F.data == 'rewrite_current_advert_parameter')
    dp.message.register(ConfirmationRewriteExistsAdvertParameterHandler(
                            filters=AdvertParameterValueFilter()).message_handler,
                        StateFilter(AdminAdvertParametersStates.start_rewrite_exists_parameter), ThrottlingFilter())
    dp.callback_query.register(ConfirmRewriteExistsAdvertParameterHandler().callback_handler,
                               StateFilter(AdminAdvertParametersStates.confirmation_rewrite_exists_parameter),
                               F.data == 'confirm_rewrite_existing_advert_parameter',
                               AdminStatusController())
    '''new_car_catalog'''
    dp.callback_query.register(ChooseStateAddNewParamsHandler().callback_handler,
                               F.data == 'advert_parameters_choose_state:1')
    dp.callback_query.register(NewCarStateParameters().callback_handler,
                                lambda callback: callback.data.startswith(('new_state_parameters:', 'set_state:')))

    dp.callback_query.register(InputCarPhotosToSetParametersBranchHandler().callback_handler,
                               F.data == 'update_params_branch_media_group')

    dp.callback_query.register(ConfirmLoadNewParamsBranchHandler().callback_handler,
                               F.data == 'confirm_load_new_params_branch',
                               AdminStatusController())

    dp.callback_query.register(ChangeStateOnExistsBranchHandler().callback_handler,
                               F.data == 'update_params_branch_state')
    dp.callback_query.register(ConfirmChangeStateOnExistsBranchHandler().callback_handler,
                               lambda callback: callback.data.startswith('change_state:'))
    '''mailing_action'''
    dp.callback_query.register(mailing.choose_mailing_action.ChooseMailingAction().callback_handler
,
                               F.data == 'mailing_action')

    dp.callback_query.register(mailing.mailing_storage.choose_specific_type.request_choose_mailing_type,
                               F.data == 'mailing_storage')
    dp.callback_query.register(mailing.mailing_storage.output_specific_mailing.output_mailings,
                               lambda callback: callback.data.startswith('select_mailings_viewed_status:'),
                               AdminStatusController())
    dp.callback_query.register(mailing.mailing_storage.utils.delete_mailing.delete_current_mailing_handler,
                               F.data == 'delete_current_mailing',
                               AdminStatusController())

    dp.callback_query.register(
        mailing.booting_mail.input_mailing_data.input_text.enter_mailing_text,
        F.data == 'create_new_mailing')

    dp.message.register(
        mailing.booting_mail.input_mailing_data.input_media.request_mailing_media,
        StateFilter(MailingStates.uploading_media),
        ThrottlingFilter(), MailingTextFilter())
    dp.callback_query.register(
        mailing.booting_mail.input_mailing_data.input_media.request_mailing_media,
        or_f((F.data == 'empty_mailing_text'),
                                    (and_f(F.data == 'add_other_media',
                                          StateFilter(MailingStates.entering_date_time)))))

    dp.message.register(
        mailing.booting_mail.input_mailing_data.input_date.request_mailing_date_time,
        StateFilter(MailingStates.entering_date_time), ThrottlingFilter(), MediaFilter())
    dp.callback_query.register(
        mailing.booting_mail.input_mailing_data.input_date.request_mailing_date_time,
        F.data == 'mailing_without_media', StateFilter(MailingStates.entering_date_time))

    dp.message.register(
        mailing.booting_mail.input_mailing_data.input_recipients.request_mailing_recipients,
        StateFilter(MailingStates.choosing_recipients), ThrottlingFilter(), DateTimeFilter())

    dp.callback_query.register(
        mailing.booting_mail.review_inputted_data.request_review_mailing_data,
        StateFilter(MailingStates.enter_recipients),
        lambda callback: callback.data.startswith('enter_mailing_recipients'))


    dp.callback_query.register(
        mailing.booting_mail.input_mailing_data.edit_mailing_data.edit_mailing_data.edit_mailing_data_handler,
        F.data == 'edit_mailing_data')
    dp.callback_query.register(
        mailing.booting_mail.input_mailing_data.edit_mailing_data.edit_data_handler.edit_field_handler,
        lambda callback: callback.data.startswith('edit_mailing_'),
        StateFilter(MailingStates.edit_inputted_data))

    dp.callback_query.register(
        mailing.booting_mail.confirm_mailing_data.confirm_boot_mailing_handler,
        F.data == 'confirm_mailing_action', AdminStatusController())

    '''user actions'''
    dp.callback_query.register(user_unban_confirmation, F.data == 'unblock_user')

    dp.callback_query.register(confirm_unblock_user, F.data == 'confirm_unban', AdminStatusController())

    dp.callback_query.register(
        user_actions.choose_specific_user.choose_category.choose_users_category.choose_user_category_by_admin_handler,
        lambda callback: callback.data.startswith('user_block_status:'), AdminStatusController())

    dp.callback_query.register(user_actions.choose_specific_user.choose_category.choose_seller_category.choose_seller_category_by_admin_handler,
                               F.data == 'seller_category_actions', AdminStatusController())

    dp.callback_query.register(user_actions.choose_specific_user.choose_specific.choose_specific_person.choose_specific_person_by_admin_handler,
                               F.data.in_(('buyer_category_actions',
                                           'legal_seller_actions',
                                           'natural_seller_actions')))

    dp.callback_query.register(user_actions.choose_specific_user.choose_specific.output_specific_seller.output_specific_seller_profile_handler,
                               lambda callback: callback.data.startswith('seller_select_action'))

    dp.callback_query.register(user_actions.choose_specific_user.choose_specific.output_specific_buyer.output_buyer_profile,
                               lambda callback: callback.data.startswith('user_select_action'))

    dp.callback_query.register(user_actions.choose_specific_user.choose_specific.input_name_to_search.start_input_name_request.input_person_name_to_search_request_handler,
                              lambda callback: callback.data.startswith('from_admin_search_by_name'))
    dp.message.register(user_actions.choose_specific_user.choose_specific.input_name_to_search.inputted_name_handler.inputted_name_from_admin_handler,
                        or_f(StateFilter(SellerReviewStates.natural_entity_search),
                            StateFilter(SellerReviewStates.legal_entity_search),
                            StateFilter(BuyerReviewStates.buyer_entity_search)),
                        ThrottlingFilter(),
                        correct_name.CheckInputName())

    dp.callback_query.register(user_actions.actions_admin_to_user.check_seller_statistic.seller_statistic_output.handle_stats_callback,
                               lambda callback: callback.data.startswith('select_seller_statistic_period'),
                               AdminStatusController())

    '''admin_tariff'''


    dp.callback_query.register(tariff_actions.input_tariff_data.process_tariff_cost,
                               F.data == 'add_tariff_by_admin',
                               StateFilter(TariffAdminBranchStates.tariffs_review))

    dp.callback_query.register(tariff_actions.output_specific_tariff.output_specific_tariff_for_admin_handler,
                               lambda callback: callback.data.startswith('admin_select_tariff:'), AdminStatusController())

    dp.callback_query.register(tariff_actions.delete_tariff.delete_tariff_model_by_admin,
                               F.data == 'delete_tariff_by_admin')
    dp.callback_query.register(tariff_actions.delete_tariff.confirm_delete_tariff_action,
                               F.data == 'confirm_delete_tariff_by_admin', AdminStatusController())

    dp.callback_query.register(tariff_actions.edit_tariff.edit_tariff_handler.edit_tariff_by_admin_handler,
                               F.data == 'edit_tariff_by_admin')
    dp.callback_query.register(tariff_actions.edit_tariff.edit_tariff_handler.field_choice_handler,
                               F.data.in_(('edit_tariff_name', 'edit_tariff_duration_time',
                                           'edit_tariff_feedbacks_residual', 'edit_tariff_cost')))

    dp.callback_query.register(tariff_actions.edit_tariff.insert_edited_tariff_data.insert_tariff_data,
                               F.data == 'confirm_tariff_edit',
                               StateFilter(TariffEditState.waiting_for_field_choice), AdminStatusController())

    'add_tariff'
    dp.message.register(tariff_actions.input_tariff_data.process_write_tariff_cost,
                        StateFilter(TariffAdminBranchStates.write_tariff_cost), ThrottlingFilter(),
                        price_is_digit.PriceIsDigit())

    dp.message.register(tariff_actions.input_tariff_data.process_write_tariff_feedbacks_residual,
                        StateFilter(TariffAdminBranchStates.write_tariff_feedbacks_residual), ThrottlingFilter(),
                        DigitFilter())

    dp.message.register(tariff_actions.input_tariff_data.process_write_tariff_time_duration,
                        StateFilter(TariffAdminBranchStates.write_tariff_duration_time), ThrottlingFilter(),
                        TimeDurationFilter())

    dp.message.register(tariff_actions.input_tariff_data.process_tariff_name,
                        StateFilter(TariffAdminBranchStates.write_tariff_name), ThrottlingFilter(),
                        UniqueTariffNameFilter(),
                        AdminStatusController())


    '''admin_seller_tariff'''
    dp.callback_query.register(tariff_for_seller.checkout_tariff_by_admin.checkout_seller_tariff_by_admin_handler,
        F.data == 'tariff_actions_by_admin')
    dp.callback_query.register(tariff_for_seller.choose_tariff_for_seller.choose_tariff_for_seller_by_admin_handler,
                               F.data == 'set_seller_tariff_by_admin')
    dp.callback_query.register(tariff_for_seller.choose_tariff_for_seller.checkout_tariff_for_seller_by_admin_handler,
                               lambda callback: callback.data.startswith('select_tariff_for_seller_by_admin:'))

    dp.callback_query.register(tariff_for_seller.confirm_action_set_tariff_by_admin.confirm_question_set_tariff_to_seller_by_admin,
                               F.data == 'activate_tariff_by_admin_for_seller')
    dp.callback_query.register(tariff_for_seller.confirm_action_set_tariff_by_admin.confirm_action_tariff_to_seller_by_admin,
                               F.data == 'confirm_set_tariff_to_seller_by_admin', AdminStatusController())

    dp.callback_query.register(tariff_for_seller.tariff_reset.tariff_reset_for_seller_from_admin_handler,
                               F.data == 'reset_seller_tariff_by_admin')
    dp.callback_query.register(tariff_for_seller.tariff_reset.confirm_action_reset_seller_tariff,
                               F.data == 'confirm_reset_seller_tariff_action', AdminStatusController())
    '''ban'''
    ic()
    dp.callback_query.register(user_ban.start_ban_process_input_reason.input_ban_reason_handler, F.data == 'user_block_action_by_admin')
    dp.message.register(user_ban.awaited_confirm_ban_process.ban_user_final_decision,
                        or_f(StateFilter(SellerReviewStates.start_input_block_reason),
                             StateFilter(BuyerReviewStates.start_input_block_reason)),
                        ThrottlingFilter(),
                        ControlInputUserBlockReason())
    dp.callback_query.register(user_ban.confirm_block_user_action.confirm_user_block_action,
                               F.data == 'confirm_block_user_by_admin', AdminStatusController())
    ic()

    '''Состояния поиска машины'''
    dp.callback_query.register(ChooseCarPriceFilterHandler().callback_handler,
                               F.data.in_(('buy_search_price_filter', 'cancel_buyer_price_filter')))

    dp.callback_query.register(StartInputCarPriceFilterStartInputHandler().callback_handler,
                               or_f(and_f(StateFilter(BuyerSearchCostFilterStates.review),
                                                 lambda callback: callback.data.startswith('buyer_cost_filter:')),
                                    and_f(StateFilter(BuyerSearchCostFilterStates.confirmation),
                                          F.data == 'rewrite_buyer_price_filter')))

    dp.message.register(ConfirmationCarPriceFilterInputHandler().message_handler,
                        StateFilter(BuyerSearchCostFilterStates.awaited_input),
                        price_is_digit.PriceIsDigit())

    dp.callback_query.register(ConfirmInputtedCarPriceFilterValueInputHandler().callback_handler,
                               StateFilter(BuyerSearchCostFilterStates.confirmation),
                               F.data == 'confirm_add_buyer_price_filter_part')

    dp.callback_query.register(CloseWindowCarPriceFilterHandler().callback_handler,
                               StateFilter(BuyerSearchCostFilterStates.review),
                               F.data.in_(('set_buyer_cost_filter', 'remove_buyer_cost_filter')))
    dp.callback_query.register(ResetCurrentRangeSideForBuyer().callback_handler,
                               F.data == 'reset_current_range_side',
                               StateFilter(BuyerSearchCostFilterStates.awaited_input))
    '''hybrid'''
    dp.callback_query.register(EmptyFieldCarpoolingHandler().callback_handler,
                               F.data == 'empty_field_carpooling')
    dp.callback_query.register(hybrid_handlers.choose_engine_type_handler,
                               and_f(lambda callback: callback.data.startswith('choose_state_'),
                                     StateFilter(HybridChooseStates.select_engine_type)))
    dp.callback_query.register(hybrid_handlers.choose_brand_handler,
                               and_f(lambda callback: callback.data.startswith('cars_engine_type'),
                                    StateFilter(HybridChooseStates.select_brand)))
    dp.callback_query.register(hybrid_handlers.choose_model_handler,
                               and_f(lambda callback: callback.data.startswith('cars_brand'),
                                     StateFilter(HybridChooseStates.select_model)))
    dp.callback_query.register(hybrid_handlers.choose_complectation_handler,
                               and_f(lambda callback: callback.data.startswith('cars_model'),
                                     StateFilter(HybridChooseStates.select_complectation)))

    dp.callback_query.register(hybrid_handlers.choose_color_handler,
                               and_f(lambda callback: callback.data.startswith('cars_complectation'),
                                     StateFilter(HybridChooseStates.select_color)))

    dp.callback_query.register(hybrid_handlers.search_config_output_handler,
                               or_f(and_f(lambda callback: callback.data.startswith('cars_year_of_release'),
                                          StateFilter(HybridChooseStates.config_output)),
                                    and_f(lambda callback: callback.data.startswith('cars_color'),
                                          StateFilter(HybridChooseStates.config_output))))

    dp.callback_query.register(BuyerPaginationVector.buyer_pagination, lambda callback: callback.data.startswith('buyer_car_pagination:'))

    '''new car'''


    '''second hand car'''

    dp.callback_query.register(second_hand_car_handlers.choose_mileage_handler,
                               and_f(lambda callback: callback.data.startswith('cars_color'),
                                     StateFilter(SecondHandChooseStates.select_mileage)))
    dp.callback_query.register(second_hand_car_handlers.choose_year_of_release_handler,
                               and_f(lambda callback: callback.data.startswith('cars_mileage'),
                                     StateFilter(SecondHandChooseStates.select_year)))
    dp.callback_query.register(load_new_car.hybrid_handlers.input_photo_to_load,
                              F.data == 'rewrite_boot_photo')
    dp.message.register(load_new_car.hybrid_handlers.input_photo_to_load,
                        (and_f(StateFilter(LoadCommodityStates.input_to_load_photo), ThrottlingFilter(),
                               price_is_digit.PriceIsDigit())))

    '''Состояния загрузки новых машин'''
    dp.callback_query.register(backward_in_boot_car, F.data == 'boot_car_backward')
    dp.callback_query.register(cancel_boot_process_callback_handler, F.data == 'cancel_boot_new_commodity')

    dp.callback_query.register(load_new_car.hybrid_handlers.input_state_to_load,
                              F.data.in_(('create_new_seller_request', 'rewrite_boot_state')))
    dp.callback_query.register(load_new_car.hybrid_handlers.input_engine_type_to_load,
                              or_f(and_f(StateFilter(LoadCommodityStates.input_to_load_engine_type),
                              lambda callback: callback.data.startswith('load_state_')),
                              F.data=='rewrite_boot_engine'))
    dp.callback_query.register(load_new_car.hybrid_handlers.input_brand_to_load,
                              or_f(and_f(StateFilter(LoadCommodityStates.input_to_load_brand),
                              lambda callback: callback.data.startswith('load_engine_')),
                              F.data=='rewrite_boot_brand'))
    dp.callback_query.register(load_new_car.hybrid_handlers.input_model_to_load,
                              or_f(and_f(StateFilter(LoadCommodityStates.input_to_load_model),
                              lambda callback: callback.data.startswith('load_brand_')),
                              F.data=='rewrite_boot_model'))
    dp.callback_query.register(load_new_car.hybrid_handlers.input_complectation_to_load,
                              or_f(and_f(StateFilter(LoadCommodityStates.input_to_load_complectation),
                              lambda callback: callback.data.startswith('load_model_')),
                              F.data=='rewrite_boot_complectation'))

    dp.callback_query.register(load_new_car.second_hand_handlers.input_year_to_load,
                              or_f(and_f(StateFilter(LoadCommodityStates.input_to_load_year),
                              lambda callback: callback.data.startswith('load_color_')),
                              F.data=='rewrite_boot_year'))
    dp.callback_query.register(load_new_car.second_hand_handlers.input_mileage_to_load,
                              or_f(and_f(StateFilter(LoadCommodityStates.input_to_load_mileage),
                              lambda callback: callback.data.startswith('load_year_')),
                              F.data=='rewrite_boot_mileage'))
    dp.callback_query.register(load_new_car.hybrid_handlers.input_color_to_load,
                              or_f(and_f(StateFilter(LoadCommodityStates.input_to_load_color),
                              lambda callback: callback.data.startswith('load_complectation_')),
                              F.data=='rewrite_boot_color'))

    dp.callback_query.register(load_new_car.hybrid_handlers.input_price_to_load,
                              or_f(and_f(StateFilter(LoadCommodityStates.input_to_load_price),
                                  or_f(lambda callback: callback.data.startswith('load_mileage_'),
                                  lambda callback: callback.data.startswith('load_color_'))),
                              F.data=='rewrite_boot_price'))


    dp.message.register(load_new_car.get_output_configs.output_load_config_for_seller,
                              StateFilter(LoadCommodityStates.photo_verification), ThrottlingFilter(),
                        message_is_photo.MessageIsPhoto())

    dp.callback_query.register(edit_boot_car_data_handler,
                               and_f(StateFilter(LoadCommodityStates.load_config_output),
                                     F.data == 'edit_boot_car_data'))

    '''уведомления'''
    dp.callback_query.register(sell_main_module.try_delete_notification,
                               lambda callback: callback.data.startswith('confirm_notification'))

    dp.message.register(lost_photos_handler,
                        F.photo)

    '''Заглушки'''
    dp.callback_query.register(page_conter_plug, F.data == 'page_count')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


