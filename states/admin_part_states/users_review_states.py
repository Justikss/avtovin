from aiogram.fsm.state import StatesGroup, State


class SellerReviewStates(StatesGroup):
    review_state = State()

class BuyerReviewStates(StatesGroup):
    review_state = State()