from aiogram.fsm.state import StatesGroup, State


class CheckNonConfirmRequestsStates(StatesGroup):
    await_input_brand = State()
    brand_flipping_process = State()