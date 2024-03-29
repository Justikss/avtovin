import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.mailing_requests import delete_mailing_action, get_mailing_by_id
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.mailing_storage.choose_specific_type import \
    request_choose_mailing_type
from handlers.utils.delete_message import delete_message
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

async def delete_mailing_messages_pack(callback, messages_to_delete):
    from handlers.callback_handlers.admin_part.accept_registration_request_button import ignore_exceptions
    for chat_id, message_ids in messages_to_delete.items():
        async with ignore_exceptions():
            await delete_message(callback, chat_id=chat_id, message_id=message_ids)
            await asyncio.sleep(1)

async def delete_current_mailing_handler(callback: CallbackQuery, state: FSMContext):
    admin_pagination_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_pagination')

    pagination_data = await redis_module.redis_data.get_data(key=f'{callback.from_user.id}:admin_pagination',
                                                 use_json=True)
    mailing_id = pagination_data['data'][pagination_data['current_page']-1]

    mailing = await get_mailing_by_id(mailing_id)
    if mailing:
        messages_to_delete = await delete_mailing_action(mailing_id)
        ic(messages_to_delete)
        if messages_to_delete:
            asyncio.create_task(delete_mailing_messages_pack(callback, messages_to_delete))

        alert_text = Lexicon_module.ADVERT_LEXICON['successfully_delete_mailing']

        await log_admin_action(callback.from_user.username, 'delete_mailing', mailing.text, mailing.scheduled_time)
    else:
        alert_text = Lexicon_module.ADVERT_LEXICON['unsuccessfully_delete_mailing']


    await callback.answer(alert_text)
    delete_page = await admin_pagination_module.AdminPaginationOutput.delete_current_page(callback, state)
    if not delete_page:
        await state.clear()
        await request_choose_mailing_type(callback, state)
