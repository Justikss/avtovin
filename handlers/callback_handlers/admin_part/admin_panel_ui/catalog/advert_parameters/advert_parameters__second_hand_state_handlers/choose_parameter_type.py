from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler, TravelMessageEditorInit


class ChooseSecondHandAdvertParametersType(BaseCallbackQueryHandler):
    pass


async def get_handler():
    choose_car_state_admin_handler = ChooseSecondHandAdvertParametersType(
        output_methods=[
            TravelMessageEditorInit(
                lexicon_part=ADVERT_PARAMETERS_LEXICON['choose_second_hand_parameter_type'],
                dynamic_buttons=2
            )
        ]
    )

    return choose_car_state_admin_handler.callback_handler
