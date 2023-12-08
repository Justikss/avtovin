from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

from database.data_requests.person_requests import PersonRequester
from handlers.callback_handlers.sell_part.seller_main_menu import seller_main_menu

async def start_sell_callback_handler(callback: CallbackQuery, state: FSMContext):
    message_editor_module = importlib.import_module('handlers.message_editor')
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    user_id = callback.from_user.id
    seller_is_exists = await PersonRequester.get_user_for_id(user_id=user_id, seller=True)
    if seller_is_exists:
        seller_is_exists = seller_is_exists[0]
        seller_is_authorized = seller_is_exists.authorized
        if not seller_is_authorized:
            lexicon_code = 'confirm_registration_from_seller'
            await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key=lexicon_code)
            # await_authorized_module = importlib.import_module('handlers.state_handlers.seller_registration.await_confirm_from_admin')
            # await await_authorized_module.seller_await_confirm_by_admin(callback=callback, state=state)
        elif seller_is_authorized:
            await callback.answer(text=lexicon_module.LEXICON['user_in_system']['message_text'])
            await seller_main_menu(callback=callback)
    else:
        lexicon_code = 'who_is_seller'
        await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key=lexicon_code, delete_mode=True)

    await callback.answer()
