from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON
from utils.oop_handlers_engineering.update_handlers.base_objects.base_handler import TravelMessageEditorInit
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler\
    import BaseCallbackQueryHandler

class ChooseSecondHandAdvertParametersType(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await state.update_data(params_type_flag='second_hand')
        self.output_methods = [
            TravelMessageEditorInit(
                lexicon_part=ADVERT_PARAMETERS_LEXICON['choose_second_hand_parameter_type'],
                dynamic_buttons=2
            )
        ]
