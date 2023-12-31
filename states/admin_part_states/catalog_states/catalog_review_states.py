from aiogram.fsm.state import StatesGroup, State


class AdminCarCatalogReviewStates(StatesGroup):
    check_new_adverts = State()
    check_viewed_adverts = State()
    await_input_reason_action = State()
    action_confirmation = State()