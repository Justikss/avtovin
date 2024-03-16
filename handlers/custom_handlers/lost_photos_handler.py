import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message




async def lost_photos_handler(message: Message, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await message.delete()
    # current_state = await state.get_state()
    #
    # if current_state == 'LoadCommodityStates:photo_verification':

