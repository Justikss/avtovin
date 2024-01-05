from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.car_advert_requests import AdvertRequester
from database.data_requests.car_configurations_requests import CarConfigs
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters import \
    OutputSpecificAdvertParameters
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_parameters_captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.utils\
    .handling_exists_value_advert_parameter.choose_actions_on_exists_parameter import TravelMessageEditorInit

class ActionOfDeletionExistsAdvertParameter(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        current_state = str(await state.get_state())
        memory_storage = await state.get_data()

        if current_state.startswith('AdminAdvertParametersStates.NewStateStates'):
            selected_parameters = memory_storage.get('selected_parameters')
        else:
            parameter_type_name = memory_storage.get('admin_chosen_advert_parameter')
            parameter_value_id = memory_storage.get('current_advert_parameter')['id']
            selected_parameters = {parameter_type_name: parameter_value_id}
        exists_model = await self.check_on_exists_adverts_by_parameter(state, selected_parameters)
        if exists_model:
            current_state = str(await state.get_state())
            await self.send_alert_answer(
                request,
                ADVERT_PARAMETERS_LEXICON['this_advert_parameter_dont_can_was_deleting']
            )
            ic(current_state)
            match current_state:
                case 'AdminAdvertParametersStates:start_delete_action':
                    ic()
                    await OutputSpecificAdvertParameters().callback_handler(request, state)#
                case _:#
                    pass
            return

        else:
            ic()
            lexicon_part = ADVERT_PARAMETERS_LEXICON['confirmation_to_delete_exists_parameter']


            if current_state.startswith('AdminAdvertParametersStates.NewStateStates'):
                param_or_params_caption = 'params'
            else:
                param_or_params_caption = 'param'

            parameter_type_to_parameter_value = await self.get_param_values_to_type_names(selected_parameters)
            lexicon_part['message_text'] = lexicon_part['message_text'].format(
                param_or_params=param_or_params_caption,
                parameter_type_to_parameter_value=parameter_type_to_parameter_value
            )
            # parameter_value_name = memory_storage.get('current_advert_parameter')['value']
            #
            # lexicon_part['message_text'] = lexicon_part['message_text'].format(
            #     parameter_type=advert_parameters_captions[parameter_type_name],
            #     parameter_value=parameter_value_name
            # )
            self.output_methods = [
                TravelMessageEditorInit(
                    lexicon_part=lexicon_part
                )

            ]

        await self.set_state(state, AdminAdvertParametersStates.start_delete_action)

    async def check_on_exists_adverts_by_parameter(self, state: FSMContext, selected_parameters):
        query = {}
        for param_type_name, param_id in selected_parameters.items():
            match param_type_name:
                case 'engine':
                    param_type_name = 'engine_type'
                case 'year':
                    param_type_name = 'year_of_release_id'

            parameter_type_key = f'{param_type_name}_id'

            query.update({parameter_type_key: int(param_id)})
        ic(query)
        advert_parameter_is_used = await AdvertRequester.get_advert_by(**query, without_actual_filter=True)
        ic(advert_parameter_is_used)
        return advert_parameter_is_used


    async def get_param_values_to_type_names(self, selected_parameters):
        param_names_to_type_names = ''
        for key, value in selected_parameters.items():
            config_object = await CarConfigs.get_by_id(table=key, model_id=value)
            param_names_to_type_names += f'{key}: {config_object.name}\n'

        return param_names_to_type_names