import importlib
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.admin_requests import AdminManager
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_tariff_data import \
    delete_incorrect_message
from handlers.callback_handlers.buy_part.language_callback_handler import set_language

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def start_admin_menu(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    ic(await state.get_state())
    await delete_incorrect_message(callback, state)
    ic()

    if await state.get_state():
        await state.clear()

    if await AdminManager.admin_authentication(callback.from_user.id):
        await message_editor.redis_data.set_data(key=f'{str(callback.from_user.id)}:user_state', value='admin')
        await message_editor.travel_editor.edit_message(lexicon_key='',
                                                        lexicon_part=Lexicon_module.ADMIN_LEXICON['start_admin_panel'],
                                                        request=callback, dynamic_buttons=1, delete_mode=True)
    else:
        logging.critical(f'Пользователь {callback.from_user.id} безуспешно вошёл в админ панель.')
        await callback.answer(
            Lexicon_module.ADMIN_LEXICON['user_havent_admin_permission'])
        return await set_language(callback, set_languange=False)