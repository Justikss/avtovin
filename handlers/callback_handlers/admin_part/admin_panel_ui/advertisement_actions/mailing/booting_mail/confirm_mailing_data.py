import logging
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config_data.config import MODIFIED_MAILING_DATETIME_FORMAT
from database.data_requests.mailing_requests import create_mailing
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.input_mailing_data.input_date import \
    request_mailing_date_time
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.choose_mailing_action import \
    request_choose_mailing_action
from utils.lexicon_utils.Lexicon import ADVERT_LEXICON
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action
from utils.mailing_heart.mailing_service import mailing_service


async def confirm_boot_mailing_handler(callback: CallbackQuery, state: FSMContext):
    memory_storage = await state.get_data()

    mailing_recipients = memory_storage['mailing_recipients']
    mailing_text = memory_storage.get('mailing_text')
    media_group = memory_storage.get('mailing_media')
    mailing_datetime = memory_storage['mailing_datetime']

    mailing_datetime = datetime.strptime(mailing_datetime[:-3], MODIFIED_MAILING_DATETIME_FORMAT)

    if mailing_datetime < datetime.now():
        return await request_mailing_date_time(callback, state, incorrect='(time)')

    new_mailing = await create_mailing(text=mailing_text, media=media_group, scheduled_time=mailing_datetime,
                                       recipients_type=mailing_recipients)
    if new_mailing:
        await mailing_service.schedule_single_mailing(bot=callback.bot, mailing=new_mailing)
        await callback.answer(ADVERT_LEXICON['successfully_boot_mail_message'])
        await state.clear()
        await request_choose_mailing_action(callback, state)
        await log_admin_action(callback.from_user.username, 'add_mailing', mailing_text, mailing_datetime)
    else:
        logging.warning(f'Администратор {callback.from_user.username} неудачно установил рассылку:\n{mailing_text}\n{media_group}\n{mailing_datetime}\n{mailing_recipients}')

        await callback.answer(ADVERT_LEXICON['unsuccessfull_boot_mail_message'])