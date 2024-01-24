import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def incorrect_controller(request: Message | CallbackQuery, state: FSMContext, incorrect, lexicon_key, current_lexicon):
    ic(lexicon_key)
    memory_storage = await state.get_data()

    lexicon_part = current_lexicon[lexicon_key]
    if lexicon_key == 'enter_mailing_media' and \
            memory_storage.get('can_edit_mailing_flag') and \
            (isinstance(request, CallbackQuery) and not request.data == 'add_other_media') and \
            memory_storage.get('mailing_media'):
        ic()
        lexicon_part['buttons'] = Lexicon_module.ADVERT_LEXICON['edit_mailing_media_buttons']

    if not incorrect:
        reply_mode = None
    else:
        if isinstance(request, Message):
            reply_mode = request.message_id
        else:
            reply_mode = None

        if incorrect == '$':
            lexicon_part['message_text'] = f'''{lexicon_part['message_text']}\n{Lexicon_module.class_lexicon['incorrect_price_$']}'''
        elif not lexicon_key == 'enter_mailing_media':
            if incorrect is True:
                lexicon_key = f'{lexicon_key}(incorrect)'
            else:
                lexicon_key = f'{lexicon_key}{incorrect}'
            ic(lexicon_part)
            ic(lexicon_key)
            ic(current_lexicon[lexicon_key])
            lexicon_part['message_text'] = current_lexicon[lexicon_key]
            ic(lexicon_part)
    if lexicon_key in ('input_tariff_cost', 'input_tariff_feedbacks', 'input_tariff_time_duration', 'input_tariff_name'):
        if not memory_storage.get('edit_tariff_mode'):
            sub_text = Lexicon_module.ADMIN_LEXICON['add_tariff_sub_text']
        else:
            sub_text = Lexicon_module.ADMIN_LEXICON['rewrite_tariff_sub_text']

        lexicon_part['message_text'] = f'''{sub_text}{lexicon_part['message_text']}'''
    return lexicon_part, reply_mode

async def get_delete_mode(state: FSMContext, incorrect):
    if not incorrect:
        memory_storage = await state.get_data()
        delete_mode = memory_storage.get('admin_incorrect_flag') is True
        ic(delete_mode, memory_storage.get('admin_incorrect_flag'))
        if delete_mode:
            await state.update_data(admin_incorrect_flag=False)
    else:
        delete_mode = False
    return delete_mode