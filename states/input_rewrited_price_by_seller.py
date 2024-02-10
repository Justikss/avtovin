from aiogram.fsm.state import StatesGroup, State


class RewritePriceBySellerStates(StatesGroup):
    await_input = State()