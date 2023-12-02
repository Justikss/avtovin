from aiogram.fsm.context import FSMContext
from aiogram.types import Message

# from states.admin_part_states.boot_new_car_photos_states import BootNewCarPhotosStates


from aiogram.fsm.state import StatesGroup, State


class BootNewCarPhotosStates(StatesGroup):
    state_1 = State()
    state_2 = State()
    state_3 = State()
    state_4 = State()
    state_5 = State()
    state_6 = State()
    state_7 = State()
    state_8 = State()



async def start_state_boot_new_car_photos_message_handler(message: Message, state: FSMContext):
    # await message.answer(str(message.chat.id))
    # return
    await message.answer(message.chat.id)
    return
    number = message.text.split(':')[-1]
    if number == '1':
        await state.set_state(BootNewCarPhotosStates.state_1)

    elif number == '2':
        await state.set_state(BootNewCarPhotosStates.state_2)

    elif number == '3':
        await state.set_state(BootNewCarPhotosStates.state_3)

    elif number == '4':
        await state.set_state(BootNewCarPhotosStates.state_4)

    elif number == '5':
        await state.set_state(BootNewCarPhotosStates.state_5)

    elif number == '6':
        await state.set_state(BootNewCarPhotosStates.state_6)
    elif number == '7':
        await state.set_state(BootNewCarPhotosStates.state_7)

    elif number == '8':
        await state.set_state(BootNewCarPhotosStates.state_8)


    await message.answer(f'Ожидаю фото для авто {number}')
