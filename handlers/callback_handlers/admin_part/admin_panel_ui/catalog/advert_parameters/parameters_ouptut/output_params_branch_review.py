from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.new_car_photo_requests import PhotoRequester
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters import \
    OutputSpecificAdvertParameters
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.utils\
    .handling_exists_value_advert_parameter.action_of_deletion.start_action_of_deletion import TravelMessageEditorInit


class ParamsBranchReviewHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.set_state(state, AdminAdvertParametersStates.NewStateStates.parameters_branch_review)

        ic()
        media_group = await PhotoRequester.try_get_photo(state, for_admin=True)
        message_text = await OutputSpecificAdvertParameters().construct_message_text_header_for_new_state_choose(state)
        ic(media_group, message_text)
        lexicon_part = ADVERT_PARAMETERS_LEXICON['review_params_branch']
        lexicon_part['message_text'] = ADVERT_PARAMETERS_LEXICON['selected_new_car_params_pattern'].format(
                        params_data=message_text
        )

        ic(lexicon_part)
        # self.output_methods = [
        #     TravelMessageEditorInit(lexicon_part=lexicon_part,
        #                             media_group=media_group,
        #                             )
        # ]
        return TravelMessageEditorInit(lexicon_part=lexicon_part,
                                    media_group=media_group)
        # ic()
        # ic(self.output_methods)

        await super().process_callback(request, state, **kwargs)