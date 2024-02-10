import importlib

from aiogram.types import CallbackQuery

from handlers.callback_handlers.sell_part.seller_main_menu import seller_main_menu

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def memory_was_lost(callback: CallbackQuery, mode: str):
    await callback.answer(Lexicon_module.LEXICON['retry_now_allert'])
    if mode == 'seller':
        await seller_main_menu(callback=callback)