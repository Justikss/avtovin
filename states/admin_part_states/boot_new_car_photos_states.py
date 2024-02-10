from aiogram.fsm.state import StatesGroup, State


class BootNewCarPhotosStates(StatesGroup):
    await_photo = State()