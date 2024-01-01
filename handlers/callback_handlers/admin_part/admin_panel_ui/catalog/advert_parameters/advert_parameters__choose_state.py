from config_data.config import car_configurations_in_keyboard_page
from database.data_requests.car_configurations_requests import CarConfigs
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import AdvertParametersChooseState
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler, InlinePaginationInit


class AdvertParametersChooseCarState(BaseCallbackQueryHandler):
    pass


async def get_handler():
    ic()
    choose_car_state_admin_handler = AdvertParametersChooseCarState(
        output_methods=[
            InlinePaginationInit(
                lexicon_class=AdvertParametersChooseState,
                models_range=await CarConfigs.get_all_states(),
                page_size=car_configurations_in_keyboard_page
            )
        ]
    )

    return choose_car_state_admin_handler.callback_handler

