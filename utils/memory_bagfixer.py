from aiogram.types import CallbackQuery

from utils.Lexicon import LEXICON
from handlers.callback_handlers.sell_part.seller_main_menu import seller_main_menu



async def memory_was_lost(callback: CallbackQuery, mode: str):
    await callback.answer(LEXICON['retry_now_allert'])
    if mode == 'seller':
        await seller_main_menu(callback=callback)