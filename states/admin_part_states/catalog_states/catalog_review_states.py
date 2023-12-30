from aiogram.fsm.state import StatesGroup, State


class AdminCarCatalogReviewStates(StatesGroup):
    check_new_adverts = State()
    check_viewed_adverts = State()