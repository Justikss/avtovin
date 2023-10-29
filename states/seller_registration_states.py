from aiogram.fsm.state import StatesGroup, State

class PersonSellerRegistrationStates(StatesGroup):
    input_fullname = State()

class CarDealerShipRegistrationStates(StatesGroup):
    input_dealship_name = State()

class HybridSellerRegistrationStates(StatesGroup):
    input_number = State()
    check_input_data = State()