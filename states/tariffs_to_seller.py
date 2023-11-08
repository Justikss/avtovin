from aiogram.fsm.state import StatesGroup, State

class ChoiceTariffForSellerStates(StatesGroup): 
    choose_tariff = State()
    preview_tariff = State()
    choose_payment_method = State()
    make_payment = State()
    payment_outcome = State()
