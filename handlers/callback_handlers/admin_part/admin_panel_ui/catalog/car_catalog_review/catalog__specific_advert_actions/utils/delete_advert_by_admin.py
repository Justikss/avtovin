import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action


async def delete_advert_handler(callback: CallbackQuery, state: FSMContext, advert_id, seller_id):
    from handlers.callback_handlers.admin_part.accept_registration_request_button import ignore_exceptions
    car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')
    memory_storage = await state.get_data()

    deleted_advert = await car_advert_requests_module.AdvertRequester.delete_advert_by_id(seller_id, advert_id)
    await log_admin_action(callback.from_user.username, 'close_advert', f'seller:{seller_id}',
                           (deleted_advert, memory_storage.get('reason')))

    async with ignore_exceptions():
        from utils.user_notification import send_notification

        await send_notification(callback, user_status='close_advert', chat_id=seller_id,
                                advert_block_data={'advert_id': advert_id, 'close_reason': memory_storage.get('reason')})


async def delete_advert_admin_action(callback: CallbackQuery, state: FSMContext, advert_id, seller_id):
    Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    asyncio.create_task(delete_advert_handler(callback, state, advert_id, seller_id))

    await callback.answer(Lexicon_module.catalog_captions['advert_successfully_closed'])

