from copy import copy

from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.utils.send_any_medias import send_media
from states.admin_part_states.mailing.mailing_setup_states import MailingStates
from utils.lexicon_utils.Lexicon import ADVERT_LEXICON
import importlib

from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions

# Импорт модуля редактирования сообщений через importlib
message_editor_module = importlib.import_module('handlers.message_editor')

async def send_mailing_review(callback, state, lexicon_part, media_group):

    if media_group:
        second_lexicon_part = copy(lexicon_part)
        lexicon_part['message_text'] = '\n'.join(lexicon_part['message_text'].split('\n')[:-1])

        await send_media(callback, media_group, caption=lexicon_part.get('message_text'))

        lexicon_part = second_lexicon_part
        lexicon_part['message_text'] = ''.join(second_lexicon_part['message_text'].split('\n')[-1])
        save_media_group = True
    else:
        save_media_group = False

    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='',
                                                           lexicon_part=lexicon_part,
                                                           save_media_group=save_media_group, delete_mode=True)

    # await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part,
    #                                                        need_media_caption=media_group,
    #                                                        media_group=media_group)





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

async def request_review_mailing_data(request: types.CallbackQuery | types.Message, state: FSMContext):
    if isinstance(request, types.CallbackQuery) and ':' in request.data and 'backward' not in request.data:
        selected_recipients = request.data.split(':')[-1]
        await state.update_data(mailing_recipients=selected_recipients)
    ic(await state.get_state())
    if str(await state.get_state()) != 'MailingStates:confirmation':
        await state.set_state(MailingStates.confirmation)

    lexicon_part, media_group = await construct_review_lexicon_part(request, state)
    await send_mailing_review(request, state, lexicon_part, media_group)
