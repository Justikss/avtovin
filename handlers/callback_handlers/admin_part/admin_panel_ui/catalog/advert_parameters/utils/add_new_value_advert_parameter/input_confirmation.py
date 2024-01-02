from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_parameters_captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_message_handler_init import \
    BaseMessageHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.utils.add_new_value_advert_parameter\
    .add_new_value_advert_parameter import TravelMessageEditorInit



class AddNewValueOfAdvertParameterConfirmationMessageHandler(BaseMessageHandler):
    async def insert_in_message_text(self, request: Message | CallbackQuery, state: FSMContext):
        memory_storage = await state.get_data()
        lexicon_part = ADVERT_PARAMETERS_LEXICON['confirmation_add_new_advert_parameter_value']
        lexicon_part['message_text'] = lexicon_part['message_text'].format(
            parameter_name=advert_parameters_captions[memory_storage.get('admin_chosen_advert_parameter')],
            new_parameter_value=request.text)
        await state.update_data(current_value=request.text)

        return lexicon_part
    async def process_message(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.set_state(state, AdminAdvertParametersStates.confirmation_add_value_process)
        self.output_methods = [
            TravelMessageEditorInit(
                lexicon_part=await self.insert_in_message_text(request, state),
                delete_mode=await self.incorrect_manager.get_incorrect_flag(state)
            )
        ]