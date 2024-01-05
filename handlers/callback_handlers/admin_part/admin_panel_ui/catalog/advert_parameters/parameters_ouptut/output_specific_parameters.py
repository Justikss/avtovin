import logging
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config_data.config import car_configurations_in_keyboard_page
from database.data_requests.car_configurations_requests import CarConfigs
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__choose_state import \
    AdvertParametersChooseCarState
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.seek_current_state_after_delete_or_edit_actions import \
    seek_current_new_type_state
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import \
    AdvertParametersChooseSpecificValue, advert_parameters_captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from utils.oop_handlers_engineering.update_handlers.base_objects.base_handler import InlinePaginationInit


class OutputSpecificAdvertParameters(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic(request.data)
        ic()
        memory_storage = await state.get_data()
        # logging.debug("Стек вызовов: %s", traceback.format_stack())
        message_text_header = ''
        parameters = None

        # if ic(await state.get_state()) == AdminAdvertParametersStates.NewStateStates.parameters_branch_review:
        #     return

        if isinstance(request, CallbackQuery) and \
                ('_choice_advert_parameters_type_' or (request.data.startswith(('admin_backward', 'new'))\
                                                       or 'state' in request.data)):

            if request.data.startswith(('admin_backward', 'new')) or 'state' in request.data:
                memory_storage = await state.get_data()
                parameter_name = memory_storage.get('next_params_output')
                structured_selected_data = await self.construct_message_text_header_for_new_state_choose(state)
                ic(structured_selected_data)
                if structured_selected_data:

                    message_text_header = ADVERT_PARAMETERS_LEXICON['selected_new_car_params_pattern'].format(
                        params_data=structured_selected_data)
                    parameters = await self.get_need_new_car_state_params(request, state, parameter_name)
                else:
                    raise Exception('Selected data is empty')
            else:
                parameter_name = request.data.split('_')[-1]
                await state.update_data(admin_chosen_advert_parameter=parameter_name)
        else:
            message_text_header = memory_storage.get('message_text_header')
            parameter_name = memory_storage.get('admin_chosen_advert_parameter')

        ic(parameter_name)
        ic(parameters)
        ic(message_text_header)
        if not parameters:
            parameters = await CarConfigs.custom_action(mode=parameter_name, action='get_*')

        display_view_class = InlinePaginationInit(
                lexicon_class=AdvertParametersChooseSpecificValue(parameter_name, message_text_header),
                models_range=parameters,
                page_size=car_configurations_in_keyboard_page
            )

        if kwargs.get('output_view_mode'):
            return display_view_class
        self.output_methods = [display_view_class]

        await self.states_control(request, state)


    async def construct_message_text_header_for_new_state_choose(self, state: FSMContext):
        memory_storage = await state.get_data()
        parameter_name = memory_storage.get('next_params_output')
        selected_parameters = memory_storage.get('selected_parameters')
        ic(selected_parameters)

        # parameter_name = memory_storage.get('current_new_car_parameter')
        # if not selected_parameters:
        #     state_object = await CarConfigs.get_by_id('state', 1)
        #     selected_parameters_string = f'''{advert_parameters_captions['state']}: {state_object.name}'''

        selected_parameters_string = ''
        for param_key, param_value in selected_parameters.items():
            if param_key in advert_parameters_captions and parameter_name != param_key:
                # Получение объекта конфигурации для каждого параметра
                config_object = await CarConfigs.get_by_id(param_key, param_value)
                # Формирование строки с названиями и значениями параметров
                selected_parameters_string += f"\n{advert_parameters_captions[param_key]}: {config_object.name}"

        selected_parameters_string = selected_parameters_string.lstrip('\n')
        return selected_parameters_string


    async def get_need_new_car_state_params(self, request, state: FSMContext, current_parameter):
        memory_storage = await state.get_data()
        selected_data = memory_storage.get('selected_parameters')

        match current_parameter:
            case 'engine':
                parameters = await CarConfigs.get_all_engines()
            case 'brand':
                parameters = await CarConfigs.get_brands_by_engine(selected_data.get('engine'))
            case 'model':
                parameters = await CarConfigs.get_models_by_brand_and_engine(selected_data.get('brand'),
                                                                             selected_data.get('engine'))
            case 'complectation':
                parameters = await CarConfigs.get_complectations_by_model_and_engine(
                    selected_data.get('model'),
                    selected_data.get('engine'))
            case 'color':
                parameters = await CarConfigs.get_color_by_complectaiton(
                    selected_data.get('complectation'), without_other=True)
            case _:#
                await self.send_alert_answer(request, ADVERT_PARAMETERS_LEXICON['memory_was_forgotten'])
                return await AdvertParametersChooseCarState().callback_handler(request, state)


        return parameters

            # if len(selected_parameters) > 1:
            #     engine_object = await CarConfigs.get_by_id('engine', selected_parameters['engine'])
            #     selected_parameters_string += f'''\n{advert_parameters_captions['engine']}: {engine_object.name}'''
            # if len(selected_parameters) > 2:
            #     brand_object = await CarConfigs.get_by_id('brand', selected_parameters['brand'])
            #     selected_parameters_string += f'''\n{advert_parameters_captions['brand']}: {brand_object.name}'''
            # if len(selected_parameters) > 3:
            #     model_object = await CarConfigs.get_by_id('model', selected_parameters['model'])
            #     selected_parameters_string += f'''\n{advert_parameters_captions['model']}: {model_object.name}'''
            # if len(selected_parameters) > 4:
            #     complectation_object = await CarConfigs.get_by_id('complectation', selected_parameters['complectation'])
            #     selected_parameters_string += f'''\n{advert_parameters_captions['complectation']}: {complectation_object.name}'''
            # if len(selected_parameters) > 5:
            #     color_object = await CarConfigs.get_by_id('color', selected_parameters['color'])
            #     selected_parameters_string += f'''\n{advert_parameters_captions['color']}: {color_object.name}'''
            #
            #
    async def states_control(self, request: CallbackQuery | Message, state: FSMContext):
        memory_storage = await state.get_data()

        match memory_storage.get('params_type_flag'):
            case 'new':
                if str(await state.get_state()) == 'AdminAdvertParametersStates:review_process':
                    await seek_current_new_type_state(request, state)
                await state.update_data(last_params_state=str(await state.get_state()))
            case 'second_hand':
                await self.set_state(state, AdminAdvertParametersStates.review_process)