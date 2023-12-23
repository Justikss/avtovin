from aiogram.fsm.state import StatesGroup, State


class SellerReviewStates(StatesGroup):
    review_state = State()
    legal_entity_search = State()
    natural_entity_search = State()

class BuyerReviewStates(StatesGroup):
    review_state = State()
    buyer_entity_search = State()