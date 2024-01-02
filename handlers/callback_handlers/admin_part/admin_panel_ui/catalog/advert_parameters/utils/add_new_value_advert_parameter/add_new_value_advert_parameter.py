from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_parameters_captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters\
    .advert_parameters__second_hand_state_handlers.choose_parameter_type import TravelMessageEditorInit


class AddNewValueAdvertParameter(BaseCallbackQueryHandler):
    async def lexicon_part_formatting(self, request, state, **kwargs):
        memory_storage = await state.get_data()
        lexicon_part = await self.incorrect_manager.get_lexicon_part_in_view_of_incorrect(
                    lexicon_object=ADVERT_PARAMETERS_LEXICON,
                    lexicon_key='start_add_new_advert_parameter_value',
                    incorrect=kwargs.get('incorrect'))
        lexicon_part['message_text'] = lexicon_part['message_text'].format(
            parameter_name=advert_parameters_captions[memory_storage.get('admin_chosen_advert_parameter')]
        )
        return lexicon_part

    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        incorrect_flag = await self.incorrect_manager.get_incorrect_flag(state)
        message_id = request.message_id if isinstance(request, Message) else None
        self.output_methods = [
            TravelMessageEditorInit(
                lexicon_part=await self.lexicon_part_formatting(request, state, **kwargs),
                delete_mode=incorrect_flag,
                reply_message=message_id if incorrect_flag else None
            )
        ]

        await self.set_state(state, AdminAdvertParametersStates.start_add_value_process)
