from aiogram.fsm.state import StatesGroup, State

class StatisticsStates(StatesGroup):
    general_bot_statistic = State()
    accept_demand_output_method = State()
    accept_demand_calculate_method = State()
    display_top_ten = State()

    class CustomParams(StatesGroup):
        choose_period = State()
        choose_params = State()
        review_process = State()
