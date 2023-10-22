import importlib

from aiogram.types import CallbackQuery

async def testor(callback: CallbackQuery):
    print(callback.data)

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
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='tech_support')

async def FAQ_callback_handler(callback: CallbackQuery):
    '''Обработчик кнопки "FAQ"'''
    message_editor = importlib.import_module('handlers.message_editor')
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='f_a_q')
