from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

from utils.chat_cleaner.media_group_messages import delete_media_groups
from utils.user_notification import try_delete_notification
from utils.user_registartion_notificator import user_dont_registrated


async def create_tarifs():
    a = importlib.import_module('database.data_requests.tariff_requests')
    data = {'name': 'minimum',
            'price': 500000,
            'duration_time': '365',
            'feedback_amount': 100}

    data2 = {'name': 'medium',
             'price': 1000000,
             'duration_time': '365',
             'feedback_amount': 500}

    data3 = {'name': 'maximum',
             'price': 15000000,
             'duration_time': '365',
             'feedback_amount': 10000}

    await a.TarifRequester.set_tariff(data)
    await a.TarifRequester.set_tariff(data3)
    await a.TarifRequester.set_tariff(data2)

async def get_tariff(callback, normal_status=False):
    tariff_module = importlib.import_module('database.data_requests.tariff_requests')
    tariff_to_seller_requests_module = importlib.import_module('database.data_requests.tariff_to_seller_requests')

    seller_bind_exists = await tariff_to_seller_requests_module.TariffToSellerBinder.get_by_seller_id(seller_id=callback.from_user.id)

    if not seller_bind_exists:

        tariffs = await tariff_module.TarifRequester.retrieve_all_data()
        ic(tariffs)
        if not tariffs:
            await create_tarifs()


        data = {'seller': str(callback.from_user.id),
                'tariff': 'minimum'
                }
        if not normal_status:
            try_set_bind = await tariff_to_seller_requests_module.TariffToSellerBinder.set_bind(data=data, bot=callback.bot, seconds=4) #days=1 seconds=5
        else:
            try_set_bind = await tariff_to_seller_requests_module.TariffToSellerBinder.set_bind(data=data, bot=callback.bot, seconds=None) #days=1 seconds=5


        if not try_set_bind:
            await user_dont_registrated(callback)



async def seller_main_menu(callback: CallbackQuery, bot=None):
    await get_tariff(callback, normal_status=True)
    message_editor_module = importlib.import_module('handlers.message_editor')
    redis_data = importlib.import_module('utils.redis_for_language')

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
