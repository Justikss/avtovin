import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.choose_actions_on_exists_parameter import \
    ChooseActionOnAdvertParameterHandler
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

input_value_advert_parameter_filter_module = importlib.import_module('handlers.custom_filters.admin_filters.catalog_filters.input_value_advert_parameter_filter')

class ConfirmRewriteExistsAdvertParameterHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        name_not_exists = await input_value_advert_parameter_filter_module\
            .AdvertParameterValueFilter()(request, state)
        if name_not_exists:
            new_car_state_parameters_module = importlib.import_module(
                'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.new_car_state_parameters_handler')

            car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')
            admin_lexicon_module = importlib.import_module('utils.lexicon_utils.admin_lexicon.admin_lexicon')

            memory_storage = await state.get_data()
            current_parameter, current_parameter_name, current_parameter_id = await new_car_state_parameters_module\
                .NewCarStateParameters().get_last_selected_param(
                state, id_mode=True)

            # current_parameter = memory_storage.get('current_advert_parameter')
            # current_parameter_name = memory_storage.get('admin_chosen_advert_parameter')
            # current_parameter_id = current_parameter['id']
            current_new_parameter_value = memory_storage.get('current_new_parameter_value')
            await car_configs_module.CarConfigs.custom_action(mode=current_parameter,
                                           action='update',
                                           name=current_new_parameter_value,
                                           model_id=current_parameter_id
                                           )
            current_parameter_dicted = {'id': current_parameter_id, 'value': current_new_parameter_value}
            await state.update_data(current_advert_parameter=current_parameter_dicted)
            await self.send_alert_answer(request, admin_lexicon_module.captions['successfully'], message=True)

            params_state_type_flag = memory_storage.get('params_type_flag')

            match params_state_type_flag:
                case 'new':
                    output_specific_parameters_module = importlib.import_module(
                        'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters')
                    await output_specific_parameters_module \
                        .OutputSpecificAdvertParameters().callback_handler(request, state)  #
                case 'second_hand':
                    await ChooseActionOnAdvertParameterHandler().callback_handler(request, state)

            ic(current_parameter_name, current_parameter, current_new_parameter_value)
            asyncio.create_task(self.logging_action(request, 'rewrote_param', ({
                current_parameter: {current_parameter_name: current_new_parameter_value}
            }, memory_storage.get('selected_parameters') if params_state_type_flag == 'new' else None)))