from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import time
import importlib
from handlers.state_handlers.seller_states_handler.seller_registration.utils import load_seller_in_database

async def seller_await_confirm_by_admin(callback: CallbackQuery, state: FSMContext):
    '''Обработчик подтверждённой(продавцом) регистрации.'''
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    message_editor_module = importlib.import_module('handlers.message_editor')


    load_try = await load_seller_in_database(authorized_state=False, state=state, request=callback)
    if load_try:
        lexicon_code = 'confirm_registration_from_seller'
    else:
        lexicon_code = 'try_again_seller_registration'

    
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key=lexicon_code)
    #time.sleep(1)
    await state.clear()

    await redis_module.redis_data.delete_key(key=str(callback.from_user.id) + ':seller_registration_mode')
    await redis_module.redis_data.delete_key(key=str(callback.from_user.id) + ':can_edit_seller_registration_data')
