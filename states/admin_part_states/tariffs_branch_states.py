from aiogram.fsm.state import StatesGroup, State


class TariffAdminBranchStates(StatesGroup):
    tariffs_review = State()
    specific_tariff_review = State()
    write_tariff_cost = State()
    write_tariff_feedbacks_residual = State()
    write_tariff_duration_time = State()
    write_tariff_name = State()

class TariffEditState(StatesGroup):
    waiting_for_field_choice = State()
    waiting_for_new_value = State()