from aiogram.fsm.state import StatesGroup, State


class BuyerSearchCostFilterStates(StatesGroup):
    review = State()
    awaited_input = State()
    confirmation = State()