from aiogram.fsm.state import StatesGroup, State


class SellerRequestsState(StatesGroup):
    await_input_brand = State()
    application_review = State()