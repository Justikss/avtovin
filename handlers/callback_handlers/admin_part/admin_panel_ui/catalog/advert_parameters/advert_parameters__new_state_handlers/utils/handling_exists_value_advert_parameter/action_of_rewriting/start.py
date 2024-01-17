import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_parameters_captions, \
    advert_params_class_lexicon
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_deletion.start_deletion import TravelMessageEditorInit

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

class RewriteExistsAdvertParameterHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):

        incorrect_flag = await self.incorrect_manager.get_incorrect_flag(state)
        self.output_methods = [
            TravelMessageEditorInit(
                lexicon_part=await self.insert_in_message_text(state, **kwargs),
                delete_mode=incorrect_flag or str(await state.get_state()) ==\
                            'AdminAdvertParametersStates.NewStateStates:parameters_branch_review',
                reply_message=await self.incorrect_manager.get_last_incorrect_message_id(state) if incorrect_flag else None
            )
        ]

        await self.set_state(state, AdminAdvertParametersStates.start_rewrite_exists_parameter)
        await super().process_callback(request, state, **kwargs)


    async def insert_in_message_text(self, state: FSMContext, **kwargs):
        new_car_state_parameters_module = importlib.import_module(
            'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.new_car_state_parameters_handler')

        # memory_storage = await state.get_data()
        # current_parameter_name = memory_storage.get('admin_chosen_advert_parameter')
        # current_parameter_value = memory_storage.get('current_advert_parameter')['value']
        current_parameter_name, current_parameter_value = await new_car_state_parameters_module\
            .NewCarStateParameters().get_last_selected_param(state)

        lexicon_part = await self.incorrect_manager.get_lexicon_part_in_view_of_incorrect(
            'start_rewrite_exists_parameter', Lexicon_module.ADVERT_PARAMETERS_LEXICON, kwargs.get('incorrect'))

        formatted_kwargs = {}
        if 'parameter_value' in lexicon_part['message_text']:
            formatted_kwargs['parameter_value'] = current_parameter_value
        formatted_kwargs['parameter_type'] = advert_parameters_captions[current_parameter_name]
        ic()
        ic(lexicon_part)
        lexicon_part['message_text'] = lexicon_part['message_text'].format(**formatted_kwargs)
        if current_parameter_name in ('complectation', 'color'):
            lexicon_part['message_text'] += advert_params_class_lexicon['translate_param_caption']
        ic()
        ic(lexicon_part)
        return lexicon_part