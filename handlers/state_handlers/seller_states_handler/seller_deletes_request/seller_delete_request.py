import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from states.seller_deletes_request_states import DeleteRequestStates

async def delete_request(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    media_group_delete_module = importlib.import_module('handlers.callback_handlers.sell_part.seller_main_menu')

    await state.set_state(DeleteRequestStates.awaited_input_deletion_number_of_commodity)

    await media_group_delete_module.delete_media_groups(request=callback)

    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='seller_delete_request')
