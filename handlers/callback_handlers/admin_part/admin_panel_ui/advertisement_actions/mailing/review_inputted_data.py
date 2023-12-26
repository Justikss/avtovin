import importlib

from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.utils.delete_message import delete_message
from states.admin_part_states.mailing_setup_states import MailingStates
from utils.lexicon_utils.Lexicon import ADVERT_LEXICON
import importlib

# Импорт модуля редактирования сообщений через importlib
message_editor_module = importlib.import_module('handlers.message_editor')

async def request_review_mailing_data(callback: types.CallbackQuery, state: FSMContext):


    if ':' in callback.data:
        selected_recipients = callback.data.split(':')[-1]
        await state.update_data(mailing_recipients=selected_recipients)

    memory_storage = await state.get_data()
    await callback.answer(f'''{memory_storage['mailing_text']}\n{memory_storage['mailing_datetime']}\n{memory_storage['mailing_recipients']}''')
    ic(memory_storage['mailing_media'])
    # await message_editor_module.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=lexicon_part)
