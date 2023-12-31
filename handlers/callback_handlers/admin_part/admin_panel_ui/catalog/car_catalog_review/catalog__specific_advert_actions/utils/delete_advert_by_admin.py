import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.car_advert_requests import AdvertRequester
from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import catalog_captions
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action
from utils.user_notification import send_notification

async def delete_advert_handler(callback: CallbackQuery, state: FSMContext, advert_id, seller_id):
    await AdvertRequester.delete_advert_by_id(seller_id, advert_id)
    await log_admin_action(callback.from_user.username, 'close_advert', f'seller:{seller_id}')
    memory_storage = await state.get_data()

    await send_notification(callback, user_status='close_advert', chat_id=seller_id,
                            advert_block_data={'advert_id': advert_id, 'close_reason': memory_storage.get('reason')})


async def delete_advert_admin_action(callback: CallbackQuery, state: FSMContext, advert_id, seller_id):

    asyncio.create_task(delete_advert_handler(callback, state, advert_id, seller_id))

    await callback.answer(catalog_captions['advert_successfully_closed'])

