import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.mailing_requests import delete_mailing_action, get_mailing_by_id
from handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_pagination import AdminPaginationOutput
from utils.lexicon_utils.Lexicon import ADVERT_LEXICON
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action

redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт


async def delete_current_mailing_handler(callback: CallbackQuery, state: FSMContext):
    pagination_data = await redis_module.redis_data.get_data(key=f'{callback.from_user.id}:admin_pagination',
                                                 use_json=True)
    mailing_id = pagination_data['data'][pagination_data['current_page']-1]

    mailing = await get_mailing_by_id(mailing_id)
    if mailing:
        await delete_mailing_action(mailing_id)

        alert_text = ADVERT_LEXICON['successfully_delete_mailing']

        await log_admin_action(callback.from_user.username, 'delete_mailing', mailing.text, mailing.scheduled_time)
    else:
        alert_text =
    await callback.answer()
    await AdminPaginationOutput.output_page(callback, state, '+')