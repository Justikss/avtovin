import importlib
from copy import copy

from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.utils.delete_message import delete_message
from states.admin_part_states.mailing_setup_states import MailingStates
from utils.lexicon_utils.Lexicon import ADVERT_LEXICON
import importlib

from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions

# Импорт модуля редактирования сообщений через importlib
message_editor_module = importlib.import_module('handlers.message_editor')

async def send_mailing_review(callback, state, lexicon_part, media_group):
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part,
                                                           need_media_caption=media_group,
                                                           media_group=media_group)
    if media_group:
        second_lexicon_part = copy(lexicon_part)
        second_lexicon_part['message_text'] = ''.join(second_lexicon_part['message_text'].split('\n')[-1])

        await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='',
                                                               lexicon_part=second_lexicon_part,
                                                               save_media_group=True)

async def construct_review_lexicon_part(callback, state):
    memory_storage = await state.get_data()
    lexicon_part = ADVERT_LEXICON['review_inputted_data']
    lexicon_part['message_text'] = lexicon_part['message_text'].format(
        mailing_recipients=captions[memory_storage['mailing_recipients']],
        mailing_text=f'''{memory_storage['mailing_text']}\n''' if memory_storage['mailing_text'] else '',
        mailing_date=memory_storage['mailing_datetime'].split()[0],
        mailing_time=memory_storage['mailing_datetime'].split()[-1]
    )
    media_group = memory_storage.get('mailing_media')
    ic(media_group)
    return lexicon_part, media_group

async def request_review_mailing_data(callback: types.CallbackQuery, state: FSMContext):
    if ':' in callback.data:
        selected_recipients = callback.data.split(':')[-1]
        await state.update_data(mailing_recipients=selected_recipients)

    lexicon_part, media_group = await construct_review_lexicon_part(callback, state)
    await send_mailing_review(callback, state, lexicon_part, media_group)
