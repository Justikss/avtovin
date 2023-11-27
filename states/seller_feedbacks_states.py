from aiogram.fsm.state import StatesGroup, State


class SellerFeedbacks(StatesGroup):
    review = State()
