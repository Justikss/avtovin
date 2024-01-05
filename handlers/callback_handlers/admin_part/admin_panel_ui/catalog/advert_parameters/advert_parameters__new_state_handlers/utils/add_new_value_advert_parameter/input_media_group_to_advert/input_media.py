import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler


class InputCarPhotosToSetParametersBranchHandler(BaseCallbackQueryHandler):
    @staticmethod
    async def construct_message_text(state: FSMContext, **kwargs):
        output_specific_parameters_module = importlib.import_module(
            'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters')

        structured_selected_data = await output_specific_parameters_module.OutputSpecificAdvertParameters() \
            .construct_message_text_header_for_new_state_choose(state)

        message_text_header = ADVERT_PARAMETERS_LEXICON['selected_new_car_params_pattern'].format(
            params_data=structured_selected_data)

        lexicon_part = ADVERT_PARAMETERS_LEXICON['input_photos_to_load_param_branch']
        if kwargs.get('incorrect'):
            message_text = f'''<b>{lexicon_part['message_text']}</b>'''
        else:
            message_text = lexicon_part['message_text']
        lexicon_part['message_text'] = f'''{message_text_header}{message_text}'''

        return lexicon_part

    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=await self.construct_message_text(state, **kwargs),
                delete_mode=True
            )
        ]
        await self.set_state(state, AdminAdvertParametersStates.NewStateStates.await_input_new_car_photos)
        ic(await state.get_state())