from aiogram.fsm.state import StatesGroup, State


class AdminAdvertParametersStates(StatesGroup):
    review_process = State()
    start_add_value_process = State()
    confirmation_add_value_process = State()
    start_delete_action = State()
    start_rewrite_exists_parameter = State()
    confirmation_rewrite_exists_parameter = State()

    class NewStateStates(StatesGroup):
        chosen_state = State()
        chosen_engine = State()
        chosen_brand = State()
        chosen_model = State()
        chosen_complectation = State()
        chosen_color = State()
        await_input_new_car_photos = State()
        confirmation_new_params_branch_to_load = State()
        parameters_branch_review = State()
