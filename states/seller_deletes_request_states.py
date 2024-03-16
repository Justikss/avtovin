from aiogram.fsm.state import StatesGroup, State


class DeleteRequestStates(StatesGroup):
    awaited_input_deletion_number_of_commodity = State()
    check_input_on_valid = State()
    review_deletion_commodity = State()
