import asyncio
import importlib

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, StateFilter, and_f, or_f
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.db_connect import create_tables
from handlers.callback_handlers.admin_part import admin_panel_ui
from handlers.callback_handlers.admin_part.admin_panel_ui import user_actions
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user import tariff_for_seller, user_ban
from handlers.callback_handlers.buy_part.buyer_offers_branch.offers_handler import buyer_offers_callback_handler

from handlers.callback_handlers.buy_part.buyer_offers_branch.show_requests import output_buyer_offers
from handlers.callback_handlers.sell_part.commodity_requests.backward_command_load_config import backward_in_boot_car
from handlers.callback_handlers.sell_part.commodity_requests.rewrite_price_by_seller import \
    rewrite_price_by_seller_handler, get_input_to_rewrite_price_by_seller_handler
from handlers.custom_filters.admin_filters.admin_status_controller import AdminStatusController
from handlers.custom_filters.admin_filters.block_user_reason_input import ControlInputUserBlockReason
from handlers.custom_filters.pass_on_dealership_address import GetDealershipAddress
from handlers.default_handlers.admin_part_default_handlers.save_seller_tariff import save_tariff_handler
from handlers.default_handlers.drop_table import drop_table_handler
from handlers.state_handlers.seller_states_handler.load_new_car.cancel_boot_process_handler import \
    cancel_boot_process_callback_handler
# from handlers.state_handlers.seller_states_handler.load_new_car import input_other_color
from handlers.utils.inline_buttons_pagination_heart import CachedRequestsView
from handlers.callback_handlers.sell_part.commodity_requests.delete_car_request import DeleteCarRequest
from handlers.callback_handlers.sell_part.commodity_requests.pagination_handlers import SellerRequestPaginationHandlers
from handlers.callback_handlers.sell_part.commodity_requests.sellers_feedbacks.delete_feedback import DeleteFeedback
from handlers.callback_handlers.sell_part.commodity_requests.sellers_feedbacks.my_feedbacks_button import \
    CheckFeedbacksHandler
from handlers.custom_handlers.lost_photos_handler import lost_photos_handler
from handlers.default_handlers.admin_part_default_handlers.boot_new_car_photos import \
    start_state_boot_new_car_photos_message_handler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_cars_pagination_system.pagination_system_controller import \
    BuyerPaginationVector
from handlers.state_handlers.seller_states_handler.load_new_car.edit_boot_data import edit_boot_car_data_handler
from handlers.utils.plugs.page_counter_plug import page_conter_plug
from states.admin_part_states.users_review_states import SellerReviewStates, BuyerReviewStates
from states.buyer_offers_states import CheckNonConfirmRequestsStates, CheckActiveOffersStates, \
    CheckRecommendationsStates
from states.input_rewrited_price_by_seller import RewritePriceBySellerStates
from states.requests_by_seller import SellerRequestsState
from states.seller_feedbacks_states import SellerFeedbacks
from utils.asyncio_tasks.invalid_tariffs_deleter import schedule_tariff_deletion
from utils.get_currency_sum_usd import fetch_currency_rate
from utils.middleware.mediagroup_chat_cleaner import CleanerMiddleware
from utils.middleware.messages_dupe_defender import ThrottlingMiddleware
from utils.user_notification import delete_notification_for_seller, try_delete_notification

'''РАЗДЕЛЕНИЕ НА БИБЛИОТЕКИ(/\) И КАСТОМНЫЕ МОДУЛИ(V)'''
from config_data.config import BOT_TOKEN
from handlers.callback_handlers.buy_part import FAQ_tech_support, backward_callback_handler, callback_handler_backward_in_carpooling, callback_handler_start_buy, \
    confirm_search_config, language_callback_handler
from handlers.callback_handlers.buy_part.buyer_offers_branch import show_requests
from handlers.custom_filters import correct_name, correct_number, pass_on_dealership_address, price_is_digit, message_is_photo
from handlers.default_handlers import start
# from handlers.callback_handlers.buy_part import (return_main_menu_from_offers_history)
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
from handlers.state_handlers.seller_states_handler.seller_registration import seller_registration_handlers, await_confirm_from_admin, check_your_registration_config
from handlers.state_handlers.seller_states_handler import load_new_car, seller_profile_branch
from handlers.default_handlers.help import  bot_help
from handlers.callback_handlers.hybrid_part import return_main_menu
from handlers.callback_handlers.hybrid_part.faq import seller_faq, buyer_faq, faq

from handlers.callback_handlers.hybrid_part.utils.media_group_collector import collect_and_send_mediagroup

'''echo.router обязан последней позици.'''

redis = None
bot = None

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)

dp = Dispatcher(storage=storage)

async def start_bot():
    global redis, edit_last_message, bot, dp, redis, storage
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    admin_router = Router()
    dp.include_router(admin_router)


    await create_tables()
    # await mock_values()
    #
    # await get_car()
    asyncio.create_task(fetch_currency_rate())
    asyncio.create_task(schedule_tariff_deletion(bot))
    asyncio.create_task(GetDealershipAddress.process_queue())

    dp.callback_query.middleware(CleanerMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())

    dp.message.register(collect_and_send_mediagroup,
                        F.photo, F.photo[0].file_id.as_("photo_id"), F.media_group_id.as_("album_id"), F.photo[0].file_unique_id.as_('unique_id'))

    dp.message.register(start_state_boot_new_car_photos_message_handler, F.text, lambda message: message.text.startswith('p:')), StateFilter(default_state)
    dp.message.register(drop_table_handler, Command(commands=['dt', 'dtc']))
    dp.message.register(bot_help, Command(commands=['free_tariff']))
    dp.message.register(save_tariff_handler, Command(commands=['ut']))

    '''обработка Сообщений'''
    dp.message.register(start.bot_start, Command(commands=["start"], ignore_case=True))

    '''Состояния регистрации покупателя'''
    dp.callback_query.register(buyer_registration_handlers.input_full_name,
                               StateFilter(BuyerRegistationStates.input_full_name))
    dp.message.register(buyer_registration_handlers.input_phone_number,
                        StateFilter(BuyerRegistationStates.input_phone_number), correct_name.CheckInputName())
    dp.message.register(buyer_registration_handlers.finish_check_phone_number,
                        StateFilter(BuyerRegistationStates.finish_check_phone_number), correct_number.CheckInputNumber())
    '''Состояния регистрации продавцов'''
    dp.callback_query.register(await_confirm_from_admin.seller_await_confirm_by_admin,
                              F.data == 'confirm_registration_from_seller')

    dp.callback_query.register(start_seller_registration_callback_handlers.seller_type_identifier,
                                    F.data.in_(('i_am_private_person', 'i_am_car_dealership')))

    dp.message.register(seller_registration_handlers.hybrid_input_seller_number,
                        and_f(StateFilter(HybridSellerRegistrationStates.input_number), correct_name.CheckInputName()))

    dp.message.register(seller_registration_handlers.dealership_input_address,
                        and_f(StateFilter(CarDealerShipRegistrationStates.input_dealship_name), correct_number.CheckInputNumber()))



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
                        and_f(StateFilter(HybridSellerRegistrationStates.check_input_data),
                        pass_on_dealership_address.GetDealershipAddress()))

    '''Пагинация клавиатуры'''
    dp.callback_query.register(CachedRequestsView.inline_buttons_pagination_vector_handler, F.data.in_(('inline_buttons_pagination:-', 'inline_buttons_pagination:+')))

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
    dp.callback_query.register(backward_callback_handler.backward_button_handler,
                               lambda callback: callback.data.startswith('backward'))
    dp.callback_query.register(hybrid_handlers.search_auto_callback_handler,
                               F.data == 'car_search')
    dp.callback_query.register(confirm_search_config.confirm_settings_handler,
                               lambda callback: callback.data.startswith('confirm_buy_settings:'))

    dp.callback_query.register(show_requests.buyer_get_requests__chose_brand, F.data.in_(('buyer_cached_offers', 'buyer_active_offers', 'buyers_recommended_offers', 'buyers_recommended_offers', 'return_to_choose_requests_brand')))

    '''Seller'''
    dp.callback_query.register(delete_notification_for_seller, lambda callback: callback.data.startswith('close_seller_notification:'))

    dp.callback_query.register(try_delete_notification, or_f(
        lambda callback: callback.data.startswith('close_seller_notification_by_redis'),
        lambda callback: callback.data.startswith('close_ban_notification:')
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
                              F.data == 'confirm_load_config_from_seller')

    dp.callback_query.register(sell_part.checkout_seller_person_profile.output_seller_profile,
                              F.data == 'seller_pofile')

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
    dp.message.register(get_input_to_rewrite_price_by_seller_handler, StateFilter(RewritePriceBySellerStates.await_input), price_is_digit.PriceIsDigit())
    '''seller"s feedbacks'''

    dp.callback_query.register(CheckFeedbacksHandler.my_feedbacks_callback_handler, lambda callback: callback.data.startswith('my_sell_feedbacks'))

    dp.callback_query.register(CheckFeedbacksHandler.check_feedbacks_handler, and_f(StateFilter(SellerFeedbacks.choose_feedbacks_state),
                               F.data.in_(('new_feedbacks', 'viewed_feedbacks'))))

    dp.callback_query.register(DeleteFeedback.delete_feedback_handler, F.data == "i'm_sure_delete_feedback")

    dp.callback_query.register(DeleteFeedback.did_you_sure_to_delete_feedback_ask, F.data == 'deal_fell_through')

    '''Оформление тарифа продавца'''
    dp.callback_query.register(seller_profile_branch.tariff_extension.output_affordable_tariffs_handler, F.data == 'tariff_extension')
    dp.callback_query.register(seller_profile_branch.selected_tariff_preview.tariff_preview_handler,
                              and_f(StateFilter(ChoiceTariffForSellerStates.choose_tariff), lambda callback: callback.data.startswith('select_tariff:')))
    dp.callback_query.register(seller_profile_branch.choose_payment.choice_payments_handler,
                              and_f(StateFilter(ChoiceTariffForSellerStates.preview_tariff), F.data == 'start_choose_payment_method'))

    dp.callback_query.register(seller_profile_branch.payments.payment_invoice_sender.send_invoice_offer,
                              and_f(StateFilter(ChoiceTariffForSellerStates.choose_payment_method),
                                     lambda callback: callback.data.startswith('run_tariff_payment:')))

    '''hybrid'''
    
    dp.callback_query.register(return_main_menu.return_main_menu_callback_handler,
                               F.data == 'return_main_menu')

    '''admin'''
    dp.callback_query.register(admin_panel_ui.utils.admin_backward_command.admin_backward_command_handler,
                               lambda callback: callback.data.startswith('admin_backward'))

    dp.callback_query.register(admin_panel_ui.start_admin_panel_window.start_admin_menu, F.data == 'admin_panel_button')

    '''user actions'''
    dp.callback_query.register(user_actions.choose_specific_user.choose_category.choose_users_category.choose_user_category_by_admin_handler,
                               F.data == 'admin_button_users', AdminStatusController())
    dp.callback_query.register(user_actions.choose_specific_user.choose_category.choose_seller_category.choose_seller_category_by_admin_handler,
                               F.data == 'seller_category_actions', AdminStatusController())

    dp.callback_query.register(user_actions.choose_specific_user.choose_specific.choose_specific_person.choose_specific_person_by_admin_handler,
                               F.data.in_(('buyer_category_actions',
                                           'legal_seller_actions',
                                           'natural_seller_actions')))

    dp.callback_query.register(user_actions.choose_specific_user.choose_specific.output_specific_seller.output_specific_user_profile_handler,
                               lambda callback: callback.data.startswith('seller_select_action'))

    dp.callback_query.register(user_actions.choose_specific_user.choose_specific.output_specific_buyer.output_buyer_profile,
                               lambda callback: callback.data.startswith('user_select_action'))

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
    dp.callback_query.register(user_ban.start_ban_process_input_reason.input_ban_reason_handler, F.data == 'user_block_action_by_admin')
    dp.message.register(user_ban.awaited_confirm_ban_process.ban_user_final_decision, or_f(StateFilter(SellerReviewStates.review_state), StateFilter(BuyerReviewStates.review_state)),
                        ControlInputUserBlockReason())
    dp.callback_query.register(user_ban.confirm_block_user_action.confirm_user_block_action,
                               F.data == 'confirm_block_user_by_admin')
    '''Состояния поиска машины'''
    '''hybrid'''
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
                        (and_f(StateFilter(LoadCommodityStates.input_to_load_photo), price_is_digit.PriceIsDigit())))

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
                              StateFilter(LoadCommodityStates.photo_verification), message_is_photo.MessageIsPhoto())

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

    @dp.message(Command(commands='m'))
    async def asdsad(message: Message):
        await message.answer(str(message.chat.id))

    @dp.callback_query()
    async def checker(callback: CallbackQuery, state: FSMContext):

      await callback.message.answer('Пролёт ' + callback.data + '\n' + str(await state.get_state()))
      #await sell_part.commodity_requests.commodity_requests.commodity_reqests_by_seller(callback=callback)
      # await accept_registration_request_button.accept_registraiton(callback=callback)


    # dp.message.register(echo.bot_echo, StateFilter(default_state))

    # dp.message.register(echo.bot_echo, StateFilter(default_state))
    #
    #
    # dp.message.register(echo.bot_echo, StateFilter(default_state))
    # '''bot_echo всегда в последней позиции'''

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


