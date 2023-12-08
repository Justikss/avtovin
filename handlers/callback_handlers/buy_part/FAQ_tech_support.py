import importlib

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config_data.config import SUPPORT_TELEGRAM
from utils.lexicon_utils.Lexicon import LEXICON


async def call_to_support_callback_handler(callback: CallbackQuery):
    '''Обработчик кнопки "позвонить в поддержку"'''
    message_editor = importlib.import_module('handlers.message_editor')
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='call_to_support')

async def write_to_support_callback_handler(callback: CallbackQuery):
    '''Обработчик кнопки "написать в поддержку"'''
    message_editor = importlib.import_module('handlers.message_editor')
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='write_to_support')

async def tech_support_callback_handler(callback: CallbackQuery):
    '''Обработчик кнопки "Поддержка"'''
    message_editor = importlib.import_module('handlers.message_editor')
    lexicon_part = LEXICON['tech_support']

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=lexicon_part['write_to_support'], url=f'https://t.me/{SUPPORT_TELEGRAM}'),
                                                      InlineKeyboardButton(text=lexicon_part['call_to_support'], callback_data='call_to_support')],
                                                     [InlineKeyboardButton(text=lexicon_part['return_main_menu'], callback_data='return_main_menu')]])
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='tech_support', my_keyboard=keyboard)

