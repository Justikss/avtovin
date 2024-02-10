from aiogram.filters.state import StatesGroup, State

class MailingReviewStates(StatesGroup):
    review_viewed_mailings = State()
    review_awaited_mailings = State()