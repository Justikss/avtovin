from aiogram.fsm.state import StatesGroup, State


class CheckNonConfirmRequestsStates(StatesGroup):
    await_input_brand = State()
    brand_flipping_process = State()


class CheckActiveOffersStates(StatesGroup):
    await_input_brand = State()
    brand_flipping_process = State()
    show_from_non_confirm_offers = State()
    show_from_search_config = State()
    show_from_recommendates = State()



class CheckRecommendationsStates(StatesGroup):
    await_input_brand = State()
    brand_flipping_process = State()
