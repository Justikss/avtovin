from aiogram.fsm.state import StatesGroup, State


class SellerFeedbacks(StatesGroup):
    choose_feedbacks_state = State()
    review_applications = State()
