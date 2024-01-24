import importlib

from aiogram import types
from aiogram.fsm.context import FSMContext

from states.admin_part_states.mailing.mailing_setup_states import MailingStates

# Импорт модуля редактирования сообщений через importlib
Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
message_editor_module = importlib.import_module('handlers.message_editor')

async def enter_mailing_text(request: types.Message | types.CallbackQuery, state: FSMContext, incorrect=False):
    from utils.oop_handlers_engineering.update_handlers.base_objects.utils_objects.incorrect_adapter import \
        IncorrectAdapter

    await state.set_state(MailingStates.entering_text)
    ic(await state.get_state())
    lexicon_part = await get_lexicon_part(incorrect)
    await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                           delete_mode=True,
                                                           reply_message=await IncorrectAdapter().get_last_incorrect_message_id(state))
    await state.set_state(MailingStates.uploading_media)

async def get_lexicon_part(incorrect):
    lexicon_key = 'enter_mailing_text'
    lexicon_part = Lexicon_module.ADVERT_LEXICON['enter_mailing_text']
    if incorrect:
        lexicon_part['message_text'] = f'''{Lexicon_module.ADVERT_LEXICON[f'{lexicon_key}(incorrect)']}{lexicon_part['message_text']}'''

    return lexicon_part