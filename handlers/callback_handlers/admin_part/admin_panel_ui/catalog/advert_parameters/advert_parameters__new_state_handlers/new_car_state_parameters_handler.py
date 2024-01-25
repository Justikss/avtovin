import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.car_configurations_requests import CarConfigs
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_params_branch_review import \
    ParamsBranchReviewHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters import \
    OutputSpecificAdvertParameters
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class NewCarStateParameters(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        #в мемори стораж:
        # selected_parameters # инфо выбранного
        # current_new_car_parameter # текущий выборный параметр
        media_photos = kwargs.get('media_photos')
        ic(media_photos)
        if media_photos:
            await self.handle_boot_photos(request, state, media_photos)
        else:
            await state.update_data(params_type_flag='new')


            start_output_all_branch = await self.selected_param_identity(request, state)
            ic(start_output_all_branch)

            await super().process_callback(request, state, **kwargs)
            ic(self.output_methods)
            ic()
            if start_output_all_branch:
                self.output_methods = []
                display_view_class = await ParamsBranchReviewHandler().process_callback(request, state)
                ic(str(await state.get_state()))
                await state.update_data(last_params_state=str(await state.get_state()))
            else:
                ic()
                display_view_class = await OutputSpecificAdvertParameters().callback_handler(request, state,
                                                                                             output_view_moode=True)#

            self.output_methods = [display_view_class]

        await super().process_callback(request, state, **kwargs)

    async def get_last_selected_param(self, state: FSMContext, id_mode=False):
        memory_storage = await state.get_data()
        current_parameter_value_id = None

        if memory_storage.get('params_type_flag') == 'new':
            selected_parameters = memory_storage.get('selected_parameters')
            all_params = ['color', 'complectation', 'model', 'brand', 'engine']
            last_param = None
            for param in all_params:
                if param in selected_parameters.keys():
                    ic(param)
                    last_param = param
                    break

            current_parameter_name = last_param
            current_parameter_value_id = selected_parameters[last_param]
            ic(current_parameter_value_id)
            parameter_object = await CarConfigs.get_by_id(current_parameter_name, current_parameter_value_id)
            current_parameter_value = parameter_object.name
        else:
            current_parameter_name = memory_storage.get('admin_chosen_advert_parameter')
            ic(memory_storage.get('current_advert_parameter'))
            param_data = memory_storage.get('current_advert_parameter')
            if len(param_data) == 2:
                current_parameter_value = param_data['value']
                current_parameter_value_id = param_data['id']
            else:
                current_parameter_value = [value for value in memory_storage.get('current_advert_parameter').values()][0]
            if id_mode and not current_parameter_value_id:
                car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')

                current_parameter_value_model = await car_configs_module.CarConfigs.custom_action(current_parameter_name,
                                                                                               'get_by_name',
                                                                                                name=current_parameter_value)
                if current_parameter_value_model:
                    current_parameter_value_id = current_parameter_value_model.id

        result = current_parameter_name, current_parameter_value

        if id_mode:
            result = (*result, current_parameter_value_id)

        return result

    async def selected_param_identity(self, request: Message | CallbackQuery, state: FSMContext):
        output_moment_flag = False
        chosen_param = None
        next_params_output = None

        if isinstance(request, CallbackQuery):
            ic(request.data)
            memory_storage = await state.get_data()
            selected_parameters = memory_storage.get('selected_parameters')
            if not selected_parameters:
                selected_parameters = {}
            if request.data.startswith('advert_parameters_choose_state:'):

                # await state.update_data(admin_chosen_advert_parameter=False)
                selected_parameters = {'state': 1}
                chosen_param = 'state'
                next_params_output = 'engine'
            elif request.data.startswith('new_state_parameters:'):
                parameter_names = ['state', 'engine',  'brand', 'model', 'complectation', 'color']
                selected_id = int(request.data.split(':')[-1])
                ic(selected_parameters)

                # last_chosen = list(selected_parameters.keys())[-1]
                last_chosen = memory_storage.get('next_params_output')
                # if await OutputSpecificAdvertParameters().check_state_on_add_new_branch_status(state):
                #     try:
                #         # Получаем индекс последнего выбранного элемента и пытаемся взять следующий элемент
                #         last_chosen = next(iter(parameter_names[parameter_names.index(last_chosen) + 1:]), None)
                #         ic()
                #         ic(last_chosen)
                #     except ValueError:
                #         # Если last_chosen не найден в списке, обрабатываем ошибку
                #         last_chosen = None
                ic(last_chosen)
                if last_chosen:
                    car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')
                    for index, parameter_name in enumerate(parameter_names):

                        if last_chosen == parameter_names[index+1]:
                            selected_parameters.update({parameter_names[index+1]: selected_id})
                            chosen_param = parameter_names[index+1]
                            ic(index+2, len(parameter_names))
                            if index + 2 < len(parameter_names):
                                next_params_output = parameter_names[index+2]
                            else:
                                output_moment_flag = True
                            break
                    parameter_name = await car_configs_module.CarConfigs.get_by_id(chosen_param, selected_id)
                    if not parameter_name:
                        return False
                    await state.update_data(admin_chosen_advert_parameter=last_chosen)
                    await state.update_data(current_advert_parameter={'value': parameter_name.name, 'id': selected_id})
            else:
                output_moment_flag = True
            ic(next_params_output, chosen_param)
            await self.set_state_by_param(state, next_params_output)
            ic(selected_parameters)
            if not next_params_output:
                next_params_output = 'review'
            await state.update_data(next_params_output=next_params_output)
            await state.update_data(selected_parameters=selected_parameters)
            if output_moment_flag:
                return True


    async def set_state_by_param(self, state, parameter):
        state_to_set = None
        match parameter:
            case 'state':
                state_to_set = AdminAdvertParametersStates.review_process
            case 'engine':
                state_to_set = AdminAdvertParametersStates.NewStateStates.chosen_state
            case 'brand':
                state_to_set = AdminAdvertParametersStates.NewStateStates.chosen_engine
            case 'model':
                state_to_set = AdminAdvertParametersStates.NewStateStates.chosen_brand
            case 'complectation':
                state_to_set = AdminAdvertParametersStates.NewStateStates.chosen_model
            case 'color':
                state_to_set = AdminAdvertParametersStates.NewStateStates.chosen_complectation

        if state_to_set:
            await self.set_state(state, state_to_set)


    async def handle_boot_photos(self, request: CallbackQuery | Message, state: FSMContext, media_photos):
        menu_method = await ParamsBranchReviewHandler().process_callback(request, state, media_photos=media_photos)
        ic(menu_method)
        self.output_methods = [
            menu_method
        ]
        ic(self.output_methods)