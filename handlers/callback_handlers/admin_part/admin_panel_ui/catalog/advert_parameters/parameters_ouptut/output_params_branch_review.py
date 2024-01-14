import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.new_car_photo_requests import PhotoRequester
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_deletion.start_deletion import TravelMessageEditorInit

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

class ParamsBranchReviewHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # OutputSpecificAdvertParameters().check_state_on_add_new_branch_status(state)
        output_specific_parameters_module = importlib.import_module(
            'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters')

        ic()
        media_group = kwargs.get('media_photos')
        if media_group:
            await self.update_photo_pack_in_load_system(state, media_group)
            state_to_set = AdminAdvertParametersStates.NewStateStates.confirmation_new_params_branch_to_load
            lexicon_part = Lexicon_module.ADVERT_PARAMETERS_LEXICON['load_new_params_branch_confirmation']
        else:
            state_to_set = AdminAdvertParametersStates.NewStateStates.parameters_branch_review
            media_group = await PhotoRequester.try_get_photo(state, for_admin=True)
            lexicon_part = Lexicon_module.ADVERT_PARAMETERS_LEXICON['review_params_branch']

        ic(state_to_set)

        await self.set_state(state, state_to_set)
        message_text = await output_specific_parameters_module.OutputSpecificAdvertParameters().construct_message_text_header_for_new_state_choose(state)
        ic(media_group, message_text)
        lexicon_part['message_text'] = f'''{Lexicon_module.ADVERT_PARAMETERS_LEXICON['selected_new_car_params_pattern'].format(
            params_data=message_text
        )}{lexicon_part['message_text']}'''
        ic()
        ic(lexicon_part)
        menu_generate_method = TravelMessageEditorInit(lexicon_part=lexicon_part,
                                    media_group=media_group)
        ic(menu_generate_method)

        return menu_generate_method

    async def update_photo_pack_in_load_system(self, state: FSMContext, media_group) -> None:
        memory_storage = await state.get_data()
        selected_parameters = memory_storage.get('selected_parameters')
        selected_parameters['photos'] = media_group
        await state.update_data(selected_parameters=selected_parameters)
