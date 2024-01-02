from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.memory_storage_incorrect_controller import \
    get_incorrect_flag
from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters\
    .advert_parameters__second_hand_state_handlers.choose_parameter_type import TravelMessageEditorInit

class AddNewAdvertParameterValue(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        memory_storage = await state.get_data()
        self.output_methods = [
            TravelMessageEditorInit(
                lexicon_part=ADVERT_PARAMETERS_LEXICON['start_add_new_advert_parameter_value'],
                delete_mode=await get_incorrect_flag(state)
            )
        ]