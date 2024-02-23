import importlib
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler



class InputCarPhotosToSetParametersBranchHandler(BaseCallbackQueryHandler):
    @staticmethod
    async def construct_message_text(state: FSMContext, **kwargs):
        Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
        output_specific_parameters_module = importlib.import_module(
            'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters')
        ic()
        ic()
        structured_selected_data = await output_specific_parameters_module.OutputSpecificAdvertParameters() \
            .construct_message_text_header_for_new_state_choose(state)

        message_text_header = Lexicon_module.ADVERT_PARAMETERS_LEXICON['selected_new_car_params_pattern'].format(
            params_data=structured_selected_data)

        lexicon_part = Lexicon_module.ADVERT_PARAMETERS_LEXICON['input_photos_to_load_param_branch']
        if kwargs.get('incorrect'):
            message_text = f'''<b>{lexicon_part['message_text']}</b>'''
        else:
            message_text = lexicon_part['message_text']
        lexicon_part['message_text'] = f'''{message_text_header}{message_text}'''

        return lexicon_part

    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic(await self.get_memory_storage(state))
        traceback.print_stack()
        await self.update_photos_state_controller(request, state)
        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=await self.construct_message_text(state, **kwargs),
                delete_mode=True
            )
        ]
        await self.new_state_controller(state, kwargs.get('update_state_mode'))
        ic(await state.get_state())

    async def update_photos_state_controller(self, request: CallbackQuery| Message, state: FSMContext):
        if isinstance(request, CallbackQuery):
            if request.data == 'update_params_branch_media_group':
                ic(await state.update_data(update_photos=True))

    async def new_state_controller(self, state, update_state_mode):
        if update_state_mode:
            state_to_set = AdminAdvertParametersStates.NewStateStates.await_input_change_state_photos
        else:
            state_to_set = AdminAdvertParametersStates.NewStateStates.await_input_new_car_photos
        ic(state_to_set)
        await self.set_state(state, state_to_set)
