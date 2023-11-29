from aiogram.fsm.context import FSMContext
from aiogram.types import Message

# from states.admin_part_states.boot_new_car_photos_states import BootNewCarPhotosStates


from aiogram.fsm.state import StatesGroup, State


class BootNewCarPhotosStates(StatesGroup):
    await_photo_GBCX = State()
    await_photo_EBSF = State()



async def start_state_boot_new_car_photos_message_handler(message: Message, state: FSMContext):
    if message.text.split(':')[-1] == 'GBCX':
        await state.set_state(BootNewCarPhotosStates.await_photo_GBCX)

    elif message.text.split(':')[-1] == 'EBSF':
        await state.set_state(BootNewCarPhotosStates.await_photo_EBSF)

    await state.set_state(BootNewCarPhotosStates.await_photo)
    await message.answer('Ожидаю фото для авто марки: BMW\nМодели: DualModel..')


async def start_state_boot_new_car_photos_message_handler2(message: Message, state: FSMContext):
    await state.set_state(BootNewCarPhotosStates.await_photo)
    await message.answer('Ожидаю фото для авто марки: BMW\nМодели: DualModel..')

async def start_state_boot_new_car_photos_message_handler3(message: Message, state: FSMContext):
    await state.set_state(BootNewCarPhotosStates.await_photo)
    await message.answer('Ожидаю фото для авто марки: BMW\nМодели: DualModel..')

async def start_state_boot_new_car_photos_message_handler4(message: Message, state: FSMContext):
    await state.set_state(BootNewCarPhotosStates.await_photo)
    await message.answer('Ожидаю фото для авто марки: BMW\nМодели: DualModel..')

async def start_state_boot_new_car_photos_message_handler5(message: Message, state: FSMContext):
    await state.set_state(BootNewCarPhotosStates.await_photo)
    await message.answer('Ожидаю фото для авто марки: BMW\nМодели: DualModel..')