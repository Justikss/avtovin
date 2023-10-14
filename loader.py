from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.redis import Redis, RedisStorage
from config_data.config import BOT_TOKEN
from handlers.custom_filters.correct_name import CorrectName

'''РАЗДЕЛЕНИЕ НА БИБЛИОТЕКИ(/\) И КАСТОМНЫЕ МОДУЛИ(V)'''
from handlers.default_handlers import start, help, echo
from handlers.callback_handlers import language_callback_handler, callback_handler_start_buy, backward_callback_handler
from handlers.state_handlers import buyer_registration_handlers


from handlers.state_handlers.buyer_registration_handlers import BuyerRegistationStates






'''echo.router обязан последней позици.'''

redis = None


async def start_bot():
    global redis, edit_last_message
    bot = Bot(token=BOT_TOKEN)

    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)



    dp.message.register(start.bot_start, Command(commands=["start"]))
    dp.message.register(help.bot_help, Command(commands=["help"]))

    dp.callback_query.register(buyer_registration_handlers.input_full_name,
                               StateFilter(BuyerRegistationStates.input_full_name))
    dp.message.register(buyer_registration_handlers.input_phone_number,
                        StateFilter(BuyerRegistationStates.input_phone_number), CorrectName())
    dp.message.register(buyer_registration_handlers.finish_check_phone_number,
                        StateFilter(BuyerRegistationStates.finish_check_phone_number))

    dp.callback_query.register(language_callback_handler.set_language,
                               F.data.in_(('language_uz', 'language_ru')))
    dp.callback_query.register(callback_handler_start_buy.start_buy,
                               F.data == 'start_buy')
    dp.callback_query.register(backward_callback_handler.backward_button_handler,
                               F.data == 'backward')



    dp.message.register(echo.bot_echo, StateFilter(default_state))
    '''bot_echo всегда в последней позиции'''

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


