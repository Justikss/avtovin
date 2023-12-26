import importlib

from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.incorrect_controller import \
    incorrect_controller
from handlers.utils.delete_message import delete_message
from states.admin_part_states.mailing_setup_states import MailingStates
from utils.lexicon_utils.Lexicon import ADVERT_LEXICON
import importlib

# Импорт модуля редактирования сообщений через importlib
message_editor_module = importlib.import_module('handlers.message_editor')

# Обработчик для запроса ввода даты и времени
# @dp.message_handler(state=MailingStates.entering_date_time)
async def request_mailing_date_time(message: types.Message, state: FSMContext, media_pack=False, incorrect=False):
    if media_pack:
        ic(media_pack)
        await state.update_data(mailing_media=media_pack)
    await state.set_state(MailingStates.choosing_recipients)
    lexicon_part, reply_to_message = await incorrect_controller(message, state, incorrect, 'request_mailing_date_time')
    await message_editor_module.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=lexicon_part,
                                                           reply_message=reply_to_message)
