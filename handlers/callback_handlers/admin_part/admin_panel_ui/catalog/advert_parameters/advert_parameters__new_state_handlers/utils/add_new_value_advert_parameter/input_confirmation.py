import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_parameters_captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_message_handler_init import \
    BaseMessageHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.add_new_value_advert_parameter.add_new_value_advert_parameter import TravelMessageEditorInit, AddNewValueAdvertParameter


class AddNewValueOfAdvertParameterConfirmationMessageHandler(BaseMessageHandler):
    async def insert_in_message_text(self, request: Message | CallbackQuery, state: FSMContext):
        Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        memory_storage = await state.get_data()
        lexicon_part = Lexicon_module.ADVERT_PARAMETERS_LEXICON['confirmation_add_new_advert_parameter_value']
        lexicon_part['message_text'] = lexicon_part['message_text'].format(
            parameter_name=advert_parameters_captions[memory_storage.get('admin_chosen_advert_parameter' \
                                                                        if memory_storage.get('params_type_flag') != 'new'\
                                                                        else 'next_params_output')],
            new_parameter_value=request.text)
        await state.update_data(current_value=request.text)

        lexicon_part = await AddNewValueAdvertParameter().insert_into_lexicon_part_selected_params_header(
            state, lexicon_part
        )

        return lexicon_part
    async def process_message(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic()
        await self.set_state(state, AdminAdvertParametersStates.confirmation_add_value_process)
        self.output_methods = [
            TravelMessageEditorInit(
                lexicon_part=await self.insert_in_message_text(request, state),
                delete_mode=await self.incorrect_manager.get_incorrect_flag(state)
            )
        ]