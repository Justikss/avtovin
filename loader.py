from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter, and_f, or_f
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.redis import Redis, RedisStorage
from config_data.config import BOT_TOKEN
from handlers.custom_filters.correct_name import CorrectName

'''РАЗДЕЛЕНИЕ НА БИБЛИОТЕКИ(/\) И КАСТОМНЫЕ МОДУЛИ(V)'''
from handlers.default_handlers import start, help, echo
from handlers.callback_handlers import (language_callback_handler, callback_handler_start_buy,
                                        backward_callback_handler, search_auto_handler, confirm_search_config,
                                        main_menu, confirm_from_seller_callback_handler, show_offers_history,
                                        return_main_menu_from_offers_history)
from handlers.state_handlers import buyer_registration_handlers
from handlers.state_handlers.buyer_registration_handlers import BuyerRegistationStates
from handlers.state_handlers.choose_car_for_buy import hybrid_handlers, new_car_handlers, second_hand_car_handlers
from states.new_car_choose_states import NewCarChooseStates
from states.hybrid_choose_states import HybridChooseStates
from states.second_hand_choose_states import SecondHandChooseStates








'''echo.router обязан последней позици.'''

redis = None


async def start_bot():
    global redis, edit_last_message
    bot = Bot(token=BOT_TOKEN)

    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)



    '''обраюотка Сообщений'''
    dp.message.register(start.bot_start, Command(commands=["start"]))
    dp.message.register(help.bot_help, Command(commands=["help"]))

    '''Состояния ргеистрации'''
    dp.callback_query.register(buyer_registration_handlers.input_full_name,
                               StateFilter(BuyerRegistationStates.input_full_name))
    dp.message.register(buyer_registration_handlers.input_phone_number,
                        StateFilter(BuyerRegistationStates.input_phone_number), CorrectName())
    dp.message.register(buyer_registration_handlers.finish_check_phone_number,
                        StateFilter(BuyerRegistationStates.finish_check_phone_number))
    '''обработка Коллбэков'''
    dp.callback_query.register(language_callback_handler.set_language,
                               F.data.in_(('language_uz', 'language_ru')))
    dp.callback_query.register(callback_handler_start_buy.start_buy,
                               F.data == 'start_buy')
    dp.callback_query.register(backward_callback_handler.backward_button_handler,
                               F.data == 'backward')
    dp.callback_query.register(search_auto_handler.search_auto_callback_handler,
                               F.data == 'car_search')
    dp.callback_query.register(search_auto_handler.search_configuration_handler,
                               F.data.in_(('second_hand_cars', 'new_cars')))
    dp.callback_query.register(confirm_search_config.confirm_settings_handler,
                               F.data == 'confirm_buy_settings')

    dp.callback_query.register(main_menu.main_menu,
                               F.data == 'return_main_menu')
    dp.callback_query.register(confirm_from_seller_callback_handler.confirm_from_seller,
                               lambda callback: callback.data.startswith('confirm_from_seller'))

    dp.callback_query.register(show_offers_history.get_offers_history, F.data == 'offers_to_user')
    dp.callback_query.register(show_offers_history.history_pagination_left, F.data == 'pagination_left')
    dp.callback_query.register(show_offers_history.history_pagination_right, F.data == 'pagination_right')
    dp.callback_query.register(return_main_menu_from_offers_history.return_from_offers_history,
                               F.data == 'return_from_offers_history')




    '''Состояния поиска машины'''
    '''hybrid'''
    dp.callback_query.register(hybrid_handlers.choose_brand_handler,
                               F.data == 'start_configuration_search')
    dp.callback_query.register(hybrid_handlers.choose_model_handler,
                               and_f(lambda callback: callback.data.startswith('cars_brand'),
                                     StateFilter(HybridChooseStates.select_model)))
    dp.callback_query.register(hybrid_handlers.choose_engine_type_handler,
                               and_f(lambda callback: callback.data.startswith('cars_model'),
                                     StateFilter(HybridChooseStates.select_engine_type)))
    dp.callback_query.register(hybrid_handlers.search_config_output_handler,
                               or_f(and_f(lambda callback: callback.data.startswith('cars_color'),
                                          StateFilter(HybridChooseStates.config_output)),
                                    and_f(lambda callback: callback.data.startswith('cars_complectation'),
                                          StateFilter(HybridChooseStates.config_output))))

    '''new car'''
    dp.callback_query.register(new_car_handlers.choose_complectation_handler,
                               and_f(lambda callback: callback.data.startswith('cars_engine_type'),
                                     StateFilter(NewCarChooseStates.select_complectation)))

    '''second hand car'''
    dp.callback_query.register(second_hand_car_handlers.choose_year_of_release_handler,
                               and_f(lambda callback: callback.data.startswith('cars_engine_type'),
                                     StateFilter(SecondHandChooseStates.select_year)))
    dp.callback_query.register(second_hand_car_handlers.choose_mileage_handler,
                               and_f(lambda callback: callback.data.startswith('cars_year_of_release'),
                                     StateFilter(SecondHandChooseStates.select_mileage)))
    dp.callback_query.register(second_hand_car_handlers.choose_color_handler,
                               and_f(lambda callback: callback.data.startswith('cars_mileage'),
                                     StateFilter(SecondHandChooseStates.select_color)))


    # dp.message.register(echo.bot_echo, StateFilter(default_state))

    dp.message.register(echo.bot_echo, StateFilter(default_state))


    dp.message.register(echo.bot_echo, StateFilter(default_state))
    '''bot_echo всегда в последней позиции'''

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


