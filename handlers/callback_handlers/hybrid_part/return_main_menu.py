from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

from handlers.callback_handlers.admin_part.admin_panel_ui.start_admin_panel_window import start_admin_menu
from handlers.default_handlers import start


async def return_main_menu_callback_handler(callback: CallbackQuery, state: FSMContext):
    redis_data = importlib.import_module('utils.redis_for_language')
    buy_main_module = importlib.import_module('handlers.callback_handlers.buy_part.main_menu')
    sell_main_module = importlib.import_module('handlers.callback_handlers.sell_part.seller_main_menu')


    user_id = callback.from_user.id
    redis_key = str(user_id) + ':user_state'
    user_state = await redis_data.redis_data.get_data(redis_key)

    if user_state == 'sell':
        await sell_main_module.seller_main_menu(callback=callback)
    elif user_state == 'buy':
        await buy_main_module.main_menu(request=callback)
    elif user_state == 'admin':
        await start_admin_menu(callback, state)
    else:
        await start.bot_start(callback, state)
    await callback.answer()