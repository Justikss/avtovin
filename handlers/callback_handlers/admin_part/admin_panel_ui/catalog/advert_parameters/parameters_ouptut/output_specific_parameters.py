import importlib
from copy import deepcopy

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__choose_state import \
    AdvertParametersChooseCarState
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.seek_current_state_after_delete_or_edit_actions import \
    seek_current_new_type_state
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.add_new_value_advert_parameter.add_new_value_advert_parameter import \
    AddNewValueAdvertParameter
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.add_new_value_advert_parameter.input_media_group_to_advert.input_media import \
    InputCarPhotosToSetParametersBranchHandler
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import \
    AdvertParametersChooseSpecificValue, advert_parameters_captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from utils.oop_handlers_engineering.update_handlers.base_objects.base_handler import InlinePaginationInit

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')


class OutputSpecificAdvertParameters(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic(request.data)
        if request.data.endswith(':0'):
            return
        ic()
        await self.incorrect_manager.try_delete_incorrect_message(request, state)
        delete_mode = kwargs.get('delete_mode')
        memory_storage = await state.get_data()
        message_text_header = ''
        parameter_name = ''
        parameters = None

        # if ic(await state.get_state()) == AdminAdvertParametersStates.NewStateStates.parameters_branch_review:
        #     return
        ic('choose_action_on_specific_adv_parameter' not in request.data)

        # await self.handling_after_deletion(memory_storage, request)

        if isinstance(request, CallbackQuery) and \
                ((request.data.startswith('admin_backward')\
                                   or any(kwarg in request.data for kwarg in ('state',
                                                                              'rewrite',
                                                                              'delete',
                                                                              '_choice_advert_parameters_type_') ) \
                                    or ('new' in request.data and memory_storage.get('params_type_flag') == 'new')))\
                and 'choose_action_on_specific_adv_parameter' not in request.data:
            ic()
            if (request.data.startswith(('admin_backward', 'new')) or any(pattern in request.data for pattern in (
                    'state',
                    'new',
                    'second_hand_choice_advert_parameters_type_',
                    'delete',
                    'rewrite'
            ))):

                ic()
                memory_storage = await state.get_data()

                ic(memory_storage.get('selected_parameters'))
                parameter_name = memory_storage.get('next_params_output')
                ic(parameter_name)
                await self.clear_exists_new_branch_status_flags(state, parameter_name, memory_storage)

                if parameter_name == 'review':
                    params_branch_review_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_params_branch_review')

                    output_class = await params_branch_review_module.ParamsBranchReviewHandler().process_callback(request, state)
                    self.output_methods = [output_class]
                elif parameter_name == 'photo':
                    return await InputCarPhotosToSetParametersBranchHandler().callback_handler(request, state)
                else:
                    ic()
                    if await self.check_state_on_add_new_branch_status(state):
                        ic()
                        return await AddNewValueAdvertParameter().callback_handler(request, state, add_new_branch_mode=True, delete_mode=delete_mode)

                if memory_storage.get('params_type_flag') == 'new':
                    structured_selected_data = await self.construct_message_text_header_for_new_state_choose(state)
                    ic(structured_selected_data)
                    if structured_selected_data:

                        message_text_header = Lexicon_module.ADVERT_PARAMETERS_LEXICON['selected_new_car_params_pattern'].format(
                            params_data=structured_selected_data)
                        parameters = await self.get_need_new_car_state_params(request, state, parameter_name)
                    else:
                        raise Exception('Selected data is empty')

                elif any(param == request.data.split('_')[-1] for param in ('year', 'mileage')):
                    ic()
                    parameter_name = request.data.split('_')[-1]
                    await state.update_data(admin_chosen_advert_parameter=parameter_name)

                elif (request.data.startswith('admin_backward') or request.data == 'confirm_delete_advert_parameter') and memory_storage.get('params_type_flag') == 'second_hand':
                    ic()
                    parameter_name = memory_storage.get('admin_chosen_advert_parameter')

        else:
            message_text_header = memory_storage.get('message_text_header')
            parameter_name = memory_storage.get('admin_chosen_advert_parameter')
            ic()

        ic(parameter_name)
        ic(parameters)
        ic((not parameters) and parameter_name in ('brand', 'mileage', 'year'))
        # if (not parameters) and parameter_name in ('brand', 'mileage', 'year'):

        if not parameters:

            if parameter_name in ('mileage', 'year'):
                parameters = await car_configs_module \
                    .CarConfigs.custom_action(mode=parameter_name, action='get_*')
            if not parameters:
                class EmptyField:
                    name = Lexicon_module.catalog_captions['empty']
                    id = 0
                parameters = [EmptyField]

        # if not parameters and parameter_name != 'review':
        #     await self.send_alert_answer(request,
        #                                  Lexicon_module.ADVERT_PARAMETERS_LEXICON['memory_was_forgotten'], message=True)
        #     return await AdvertParametersChooseCarState().callback_handler(request, state)

        ic(message_text_header)
        ic(parameters)

        ic(parameters)
        ic(parameter_name)
        if not parameter_name == 'review':
            config_module = importlib.import_module('config_data.config')

            display_view_class = InlinePaginationInit(
                    lexicon_class=AdvertParametersChooseSpecificValue(parameter_name, message_text_header),
                    models_range=parameters,
                    page_size=config_module.car_configurations_in_keyboard_page
                )

            self.output_methods = [display_view_class]
            ic(display_view_class)
        else:
            display_view_class = None

        await self.states_control(request, state)

        if kwargs.get('output_view_mode'):
            return display_view_class



    async def construct_message_text_header_for_new_state_choose(self, state: FSMContext):
        memory_storage = await state.get_data()
        parameter_name = memory_storage.get('next_params_output')
        selected_parameters = memory_storage.get('selected_parameters')
        ic(selected_parameters)

        selected_parameters_string = ''
        for param_key, param_value in selected_parameters.items():
            if param_key in advert_parameters_captions and parameter_name != param_key:
                # Получение объекта конфигурации для каждого параметра
                ic(str(param_value).isdigit(), param_value)
                if isinstance(param_value, dict):
                    config_name = [value for value in param_value.values()][0]
                else:
                # if str(param_value).isdigit():
                    config_object = await car_configs_module\
                        .CarConfigs.get_by_id(param_key, param_value)
                    if not config_object:
                        config_name = param_value
                    else:
                        config_name = config_object.name
                # else:
                #     config_name = param_value
                # Формирование строки с названиями и значениями параметров
                selected_parameters_string += f"\n{advert_parameters_captions[param_key]}: {config_name}"

        selected_parameters_string = selected_parameters_string.lstrip('\n')
        return selected_parameters_string


    async def get_need_new_car_state_params(self, request, state: FSMContext, current_parameter):
        get_all_flag = False
        parameters = None
        memory_storage = await state.get_data()
        selected_data = memory_storage.get('selected_parameters')
        ic(current_parameter)
        add_new_branch_mode = await self.check_state_on_add_new_branch_status(state)
        match current_parameter:
            case 'engine':
                parameters = await car_configs_module\
                    .CarConfigs.get_all_engines()
            case 'brand':
                parameters = await car_configs_module\
                    .CarConfigs.get_brands_by_engine(selected_data.get('engine'))
            case 'model' if not add_new_branch_mode:
                parameters = await car_configs_module\
                    .CarConfigs.get_models_by_brand_and_engine(selected_data.get('brand'),
                                                                             selected_data.get('engine'))
            case 'complectation' if not add_new_branch_mode:
                parameters = await car_configs_module\
                    .CarConfigs.get_complectations_by_model_and_engine(
                    selected_data.get('model'),
                    selected_data.get('engine'))

            case 'color' if not add_new_branch_mode:
                parameters = await car_configs_module\
                    .CarConfigs.get_color_by_complectaiton(
                    selected_data.get('complectation'), without_other=True)

                # parameters = 'review'
            case _:#
                # if add_new_branch_mode and not parameters:
                #     get_all_flag = True
                parameters = None

        # if get_all_flag:
        #     parameters = await car_configs_module\
        #     .CarConfigs.custom_action(current_parameter, 'get_*')
        if not isinstance(parameters, list) and parameters is not None:
            parameters = list(parameters)
        return parameters


    async def states_control(self, request: CallbackQuery | Message, state: FSMContext):
        memory_storage = await state.get_data()
        ic(memory_storage.get('params_type_flag'))
        ic()
        match memory_storage.get('params_type_flag'):

            case 'new':
                if 'NewStateStates' not in str(await state.get_state()):

                    # if delete_params_flag:
                    #     await state.update_data(delete_params_flag=None)
                    await seek_current_new_type_state(request, state)
                ic(str(await state.get_state()))
                ic()
                await state.update_data(last_params_state=str(await state.get_state()))

            case 'second_hand':
                await self.set_state(state, AdminAdvertParametersStates.review_process)


    async def check_state_on_add_new_branch_status(self, state: FSMContext):
        memory_storage = await state.get_data()
        add_new_branch_status = memory_storage.get('add_new_branch_status')
        ic(add_new_branch_status)
        if add_new_branch_status:
            return add_new_branch_status


    async def clear_exists_new_branch_status_flags(self, state: FSMContext, parameter_name, memory_storage):
        param_which_startswith_add_branch = memory_storage.get('add_new_branch_status')
        ic(parameter_name)
        ic()
        if param_which_startswith_add_branch in (parameter_name, 'state', 'engine'):
            await state.update_data(add_new_branch_status=False)

        if memory_storage.get('can_set_add_new_branch_status'):
            await state.update_data(can_set_add_new_branch_status=False)