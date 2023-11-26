from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

from database.data_requests.tariff_to_seller_requests import TariffToSellerBinder
from utils.Lexicon import LEXICON
from handlers.callback_handlers.buy_part.show_offers_history import try_delete_notification
from utils.chat_cleaner.media_group_messages import delete_media_groups


async def create_tarifs():
    a = importlib.import_module('database.data_requests.tariff_requests')
    data = {'name': 'minimum',
            'price': 50,
            'duration_time': '365',
            'feedback_amount': 100}

    data2 = {'name': 'medium',
             'price': 200,
             'duration_time': '365',
             'feedback_amount': 500}

    data3 = {'name': 'maximum',
             'price': 1000,
             'duration_time': '365',
             'feedback_amount': 10000}

    a.TarifRequester.set_tariff(data)
    a.TarifRequester.set_tariff(data3)
    a.TarifRequester.set_tariff(data2)

async def get_tariff(callback):
    a = importlib.import_module('database.data_requests.tariff_requests')

    seller_bind_exists = TariffToSellerBinder.get_by_seller_id(seller_id=callback.from_user.id)

    if not seller_bind_exists:

        tariffs = a.TarifRequester.retrieve_all_data()
        if not tariffs:
            await create_tarifs()


        data = {'seller': str(callback.from_user.id),
                'tariff': 'minimum'
                }

        TariffToSellerBinder.set_bind(data=data)



async def seller_main_menu(callback: CallbackQuery, bot=None):
    await get_tariff(callback)
    message_editor_module = importlib.import_module('handlers.message_editor')
    redis_data = importlib.import_module('utils.redis_for_language')

    # exist_media_group_message = await redis_data.get_data(key=str(callback.from_user.id) + ':last_media_group')
    # if exist_media_group_message:
    #     try:
    #         [await callback.bot.delete_message(chat_id=callback.message.chat.id,
    #                                           message_id=message_id) for message_id in exist_media_group_message]
    #     except:
    #         pass

    await try_delete_notification(callback=callback, user_status='seller')
    await delete_media_groups(request=callback)
    await redis_data.redis_data.delete_key(key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')
    await redis_data.redis_data.delete_key(key=str(callback.from_user.id) + ':seller_requests_pagination')

    lexicon_code = 'seller_main_menu'
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key=lexicon_code, bot=bot, delete_mode=True)

    user_id = callback.from_user.id
    redis_key = str(user_id) + ':user_state'
    await redis_data.redis_data.set_data(redis_key, value='sell')

    await callback.answer()
