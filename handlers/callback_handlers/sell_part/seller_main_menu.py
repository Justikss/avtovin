import logging
from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib


from utils.chat_cleaner.media_group_messages import delete_media_groups
from utils.user_notification import try_delete_notification
from utils.user_registartion_notificator import user_dont_registrated



async def try_get_free_tariff(callback, normal_status=False):
    tariff_to_seller_requests_module = importlib.import_module('database.data_requests.tariff_to_seller_requests')


    seller_bind_exists = await tariff_to_seller_requests_module.TariffToSellerBinder.get_by_seller_id(seller_id=callback.from_user.id)

    if not seller_bind_exists:
        person_requests_module = importlib.import_module('database.data_requests.person_requests')

        seller_model = await person_requests_module.PersonRequester.get_user_for_id(callback.from_user.id, seller=True)
        if seller_model:
            seller_model = seller_model[0]
            if seller_model.data_registration < datetime(2024, 5, 1).date():
                tariff_requests_module = importlib.import_module('database.data_requests.tariff_requests')

                seller_entity = seller_model.entity
                tariff = await tariff_requests_module.TarifRequester.get_free_tariff(seller_entity)
                if not tariff and seller_model:
                    logging.error('[2/2]Данные продавца: %d, %s',
                      int(seller_model.telegram_id),
                        f'{seller_model.dealship_name} {seller_model.dealship_address}' \
                            if seller_entity == 'legal' \
                            else f'{seller_model.surname} {seller_model.name} {seller_model.patronymic}')
                    return
                boot_data = {'seller': str(callback.from_user.id),
                        'tariff': tariff
                        }
                if not normal_status:
                    try_set_bind = await tariff_to_seller_requests_module.TariffToSellerBinder.set_bind(data=boot_data, bot=callback.bot, seconds=4) #days=1 seconds=5
                else:
                    try_set_bind = await tariff_to_seller_requests_module.TariffToSellerBinder.set_bind(data=boot_data, bot=callback.bot, seconds=None) #days=1 seconds=5




async def seller_main_menu(callback: CallbackQuery, bot=None):
    await try_get_free_tariff(callback, normal_status=True)
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
