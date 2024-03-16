from aiogram.fsm.state import StatesGroup, State


class SellerReviewStates(StatesGroup):
    review_state = State()
    legal_entity_search = State()
    natural_entity_search = State()
    start_input_block_reason = State()
    confirmation_block_user = State()


class BuyerReviewStates(StatesGroup):
    review_state = State()
    buyer_entity_search = State()
    start_input_block_reason = State()
    confirmation_block_user = State()
