from aiogram.fsm.state import StatesGroup, State


class AdminCarCatalogReviewStates(StatesGroup):
    check_new_adverts = State()
    check_viewed_adverts = State()
    await_input_reason_action = State()
    action_confirmation = State()

class AdminCarCatalogSearchByIdStates(StatesGroup):
    await_input_for_admin = State()
    review_searched_advert = State()