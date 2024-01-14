import importlib

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config_data.config import SUPPORT_NUMBER_2, SUPPORT_NUMBER, SUPPORT_TELEGRAM

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
config_module = importlib.import_module('config_data.config')

async def call_to_support_callback_handler(callback: CallbackQuery):
    '''Обработчик кнопки "позвонить в поддержку"'''
    message_editor = importlib.import_module('handlers.message_editor')
    lexicon_part = Lexicon_module.LEXICON['call_to_support']
    lexicon_part['message_text'] = lexicon_part['message_text'].format(SUPPORT_NUMBER=SUPPORT_NUMBER, SUPPORT_NUMBER_2=SUPPORT_NUMBER_2)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

async def write_to_support_callback_handler(callback: CallbackQuery):
    '''Обработчик кнопки "написать в поддержку"'''
    message_editor = importlib.import_module('handlers.message_editor')
    lexicon_part = Lexicon_module.LEXICON['write_to_support']
    lexicon_part['message_text'] = lexicon_part['message_text'].format(SUPPORT_TELEGRAM=SUPPORT_TELEGRAM)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

async def tech_support_callback_handler(callback: CallbackQuery):
    '''Обработчик кнопки "Поддержка"'''
    message_editor = importlib.import_module('handlers.message_editor')
    config_module = importlib.import_module('config_data.config')
    Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    lexicon_part = Lexicon_module.LEXICON['tech_support']

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=lexicon_part['write_to_support'], url=f'https://t.me/{config_module.SUPPORT_TELEGRAM}'),
                                                      InlineKeyboardButton(text=lexicon_part['call_to_support'], callback_data='call_to_support')],
                                                     [InlineKeyboardButton(text=lexicon_part['return_main_menu'], callback_data='return_main_menu')]])
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='tech_support', my_keyboard=keyboard)

