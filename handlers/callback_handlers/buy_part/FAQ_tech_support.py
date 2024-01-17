import importlib

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config_data.config import SUPPORT_NUMBER_2, SUPPORT_NUMBER, SUPPORT_TELEGRAM
from database.data_requests.tech_supports import TechSupportsManager
from keyboards.inline.kb_creator_with_urls import createinlinekeyboard
from utils.lexicon_utils.Lexicon import catalog_captions, captions

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
config_module = importlib.import_module('config_data.config')

async def get_support_links(support_type):
    tech_supports = await TechSupportsManager.get_by_type(support_type)
    if not tech_supports:
        tech_supports = [catalog_captions['empty']]
        empty_flag = True
    else:
        tech_supports = [support.link for support in tech_supports]
        empty_flag = False


    return tech_supports, empty_flag

async def call_to_support_callback_handler(callback: CallbackQuery):
    '''Обработчик кнопки "позвонить в поддержку"'''
    message_editor = importlib.import_module('handlers.message_editor')

    support_links, empty_flag = await get_support_links('number')

    lexicon_part = Lexicon_module.LEXICON['call_to_support']

    for support_link in support_links:
        if len(support_links) == 1 and support_link.replace(' ', '').isalpha():
            sub_string = f'<b>{support_link}</b>'
        else:
            sub_string = captions['tech_support_entity'].format(SUPPORT_NUMBER=support_link)

        lexicon_part['message_text'] += sub_string

    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

async def write_to_support_callback_handler(callback: CallbackQuery):
    '''Обработчик кнопки "написать в поддержку"'''
    message_editor = importlib.import_module('handlers.message_editor')
    support_links, empty_flag = await get_support_links('telegram')

    buttons_data = []
    for link in support_links:
        buttons_data.append((link, f'''https://t.me/{link.replace('@', '') if '@' in link else 'page_count'}'''))

    buttons_data.append((Lexicon_module.LEXICON['write_to_support']['backward:support'], 'backward:support'))

    keyboard = await createinlinekeyboard(args=buttons_data, row_width=config_module.tech_support_tg_link_buttons_width,
                                          dynamic_buttons=1)

    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='write_to_support',
                                                    my_keyboard=keyboard)

async def tech_support_callback_handler(callback: CallbackQuery):
    '''Обработчик кнопки "Поддержка"'''
    message_editor = importlib.import_module('handlers.message_editor')
    # config_module = importlib.import_module('config_data.config')
    # Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='tech_support')

