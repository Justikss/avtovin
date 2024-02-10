import importlib

from aiogram.types import CallbackQuery


async def FAQ_callback_handler(callback: CallbackQuery):
    '''Обработчик кнопки "FAQ"'''
    message_editor = importlib.import_module('handlers.message_editor')
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='f_a_q')
