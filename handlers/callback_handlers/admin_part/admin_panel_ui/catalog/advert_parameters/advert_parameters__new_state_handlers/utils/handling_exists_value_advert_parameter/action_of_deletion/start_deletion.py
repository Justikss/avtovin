import importlib
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_parameters_captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.choose_actions_on_exists_parameter import TravelMessageEditorInit

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


class ActionOfDeletionExistsAdvertParameter(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        current_state = str(await state.get_state())
        memory_storage = await state.get_data()
        traceback.print_exc()
        if memory_storage.get('params_type_flag') == 'new':
            selected_parameters = memory_storage.get('selected_parameters')
        else:
            parameter_type_name = ic(memory_storage.get('admin_chosen_advert_parameter'))
            parameter_value_id = ic(memory_storage.get('current_advert_parameter'))['id']
            selected_parameters = {parameter_type_name: parameter_value_id}

        ic(selected_parameters)
        ic()
        exists_model = await self.check_on_exists_adverts_by_parameter(state, selected_parameters, with_state_param=True)
        if exists_model:
            current_state = str(await state.get_state())
            await self.send_alert_answer(
                request,
                Lexicon_module.ADVERT_PARAMETERS_LEXICON['this_advert_parameter_dont_can_was_deleting'],
                message=True
            )
            ic(current_state)
            # match current_state:
            #     case 'AdminAdvertParametersStates:start_delete_action':
            output_specific_parameters_module = importlib.import_module(
                'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters')
            #
            #         ic()
            await output_specific_parameters_module.OutputSpecificAdvertParameters().callback_handler(request, state)#
                # case _:#
                #     pass
            self.output_methods = []
            return

        else:
            parameter_type_to_parameter_value = await self.get_param_values_to_type_names(selected_parameters)
            ic()
            lexicon_part = Lexicon_module.ADVERT_PARAMETERS_LEXICON['confirmation_to_delete_exists_parameter']

            ic(current_state)
            if memory_storage.get('params_type_flag') == 'new':
                from_param_branch = advert_parameters_captions['from_param_branch'].format(
                    param_branch='\n'.join(parameter_type_to_parameter_value.split('\n')[:-2]))
                parameter_type_to_parameter_value = ic(parameter_type_to_parameter_value.split('\n'))[-2]
                ic(parameter_type_to_parameter_value)
            else:
                from_param_branch = ''

            lexicon_part['message_text'] = lexicon_part['message_text'].format(
                from_param_branch=from_param_branch,
                parameter_type_to_parameter_value=parameter_type_to_parameter_value
            )

            self.output_methods = [
                TravelMessageEditorInit(
                    lexicon_part=lexicon_part,
                    delete_mode=current_state == 'AdminAdvertParametersStates.NewStateStates:parameters_branch_review'
                )

            ]

        await self.set_state(state, AdminAdvertParametersStates.start_delete_action)

    async def check_on_exists_adverts_by_parameter(self, state: FSMContext, selected_parameters, with_state_param=True):
        car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')
        ic(selected_parameters, with_state_param)
        query = {}
        for param_type_name, param_id in selected_parameters.items():
            match param_type_name:
                case 'engine':
                    param_type_name = 'engine_type'
                case 'year':
                    param_type_name = 'year_of_release_id'
            if (((param_type_name in ('state', 'photos')) and ((not with_state_param) or param_type_name == 'photos') )
                    or not param_id):
                continue

            if param_type_name.endswith('id'):
                parameter_type_key = param_type_name
            else:
                parameter_type_key = f'{param_type_name}_id'
            if isinstance(param_id, dict):
                return []
            query.update({parameter_type_key: int(param_id) if isinstance(param_id, (str, int)) else param_id.id})
        ic(query)
        advert_parameter_is_used = await car_advert_requests_module\
            .AdvertRequester.get_advert_by(**query, without_actual_filter='for_deletion')
        # if not advert_parameter_is_used and selected_parameters.get('complectation'):
        #     from database.db_connect import manager
        #     from database.tables.statistic_tables.advert_parameters import AdvertParameters
        #     advert_parameter_is_used = list(await manager.execute(AdvertParameters.select(AdvertParameters.id).where(AdvertParameters.complectation == selected_parameters.get('complectation'))))
        ic(advert_parameter_is_used)
        return advert_parameter_is_used


    async def get_param_values_to_type_names(self, selected_parameters):
        car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')

        param_names_to_type_names = ''
        for key, value in selected_parameters.items():
            if key == 'state' and value is None:
                config_name = advert_parameters_captions['duo_states']
            else:
                config_object = await car_configs_module.CarConfigs.get_by_id(table=key, model_id=value)
                config_name = config_object.name
            param_names_to_type_names += f'{advert_parameters_captions[key]}: {config_name}\n'

        return param_names_to_type_names