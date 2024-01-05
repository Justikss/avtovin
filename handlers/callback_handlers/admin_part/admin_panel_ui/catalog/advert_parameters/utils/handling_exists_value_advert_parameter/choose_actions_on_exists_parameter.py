from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.car_configurations_requests import CarConfigs
from handlers.utils.delete_message import delete_message
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.Lexicon import LEXICON, ADVERT_PARAMETERS_LEXICON
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_parameters_captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.\
    output_specific_parameters import OutputSpecificAdvertParameters
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.utils.add_new_value_advert_parameter\
    .input_confirmation import TravelMessageEditorInit

class ChooseActionOnAdvertParameterHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await delete_message(request, await self.incorrect_manager.get_last_incorrect_message_id(state))

        if isinstance(request, CallbackQuery) and request.data[-1].isdigit():
            current_parameter_value_id = request.data.split(':')[-1]
            memory_storage = await state.get_data()
            current_parameter_name = memory_storage.get('admin_chosen_advert_parameter')
            current_parameter_value = await CarConfigs.get_by_id(current_parameter_name, current_parameter_value_id)
            if current_parameter_value:
                current_parameter_value = current_parameter_value.name
                await state.update_data(current_advert_parameter={'id': current_parameter_value_id, 'value': current_parameter_value})
            else:
                await request.answer(LEXICON['search_parameter_invalid'])
                ic()
                await OutputSpecificAdvertParameters().callback_handler(request, state)#
                return
        else:
            memory_storage = await state.get_data()
            current_parameter_name = memory_storage.get('admin_chosen_advert_parameter')
            current_parameter_value = memory_storage.get('current_advert_parameter')['value']

        lexicon_part = ADVERT_PARAMETERS_LEXICON['choose_action_on_specific_parameter_value']
        lexicon_part['message_text'] = lexicon_part['message_text'].format(
            parameter_name=advert_parameters_captions[current_parameter_name],
            parameter_value=current_parameter_value
        )
        self.output_methods = [
            TravelMessageEditorInit(
                delete_mode=self.incorrect_manager.get_incorrect_flag(state),
                lexicon_part=lexicon_part,
                dynamic_buttons=2
            )

        ]

        await self.set_state(state, AdminAdvertParametersStates.review_process)