from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.admin_part_states.boot_new_car_photos_states import BootNewCarPhotosStates


async def start_state_boot_new_car_photos_message_handler(message: Message, state: FSMContext):
    await state.set_state(BootNewCarPhotosStates.await_photo)
    await message.answer('Ожидаю фото')