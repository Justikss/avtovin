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
        await state.update_data(params_type_flag='new')


        start_output_all_branch = await self.selected_param_identity(request, state)
        ic(start_output_all_branch)

        await super().process_callback(request, state, **kwargs)
        ic(self.output_methods)
        ic()
        if start_output_all_branch:
            self.output_methods = []
            display_view_class = await ParamsBranchReviewHandler().process_callback(request, state)
        else:
            ic()
            display_view_class = await OutputSpecificAdvertParameters().callback_handler(request, state,
                                                                                         output_view_moode=True)#

        self.output_methods = [display_view_class]

        await super().process_callback(request, state, **kwargs)

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
                selected_parameters = {'state': 1}
                chosen_param = 'state'
                next_params_output = 'engine'
            elif request.data.startswith('new_state_parameters:'):
                parameter_names = ['state', 'engine',  'brand', 'model', 'complectation', 'color']
                selected_id = int(request.data.split(':')[-1])
                ic(selected_parameters)

                # last_chosen = list(selected_parameters.keys())[-1]
                last_chosen = memory_storage.get('next_params_output')
                ic(last_chosen)
                if last_chosen:
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
                    parameter_name = await CarConfigs.get_by_id(chosen_param, selected_id)
                    if not parameter_name:
                        return False
                    await state.update_data(admin_chosen_advert_parameter=last_chosen)
                    await state.update_data(current_advert_parameter={'value': parameter_name.name, 'id': selected_id})
            else:
                output_moment_flag = True
            ic(chosen_param)
            await self.set_state_by_param(state, chosen_param)
            ic(selected_parameters)

            await state.update_data(next_params_output=next_params_output)
            await state.update_data(selected_parameters=selected_parameters)
            if output_moment_flag:
                return True


    async def set_state_by_param(self, state, parameter):
        state_to_set = None
        match parameter:
            case 'state':
                state_to_set = AdminAdvertParametersStates.NewStateStates.chosen_state
            case 'engine':
                state_to_set = AdminAdvertParametersStates.NewStateStates.chosen_engine
            case 'brand':
                state_to_set = AdminAdvertParametersStates.NewStateStates.chosen_brand
            case 'model':
                state_to_set = AdminAdvertParametersStates.NewStateStates.chosen_model
            case 'complectation':
                state_to_set = AdminAdvertParametersStates.NewStateStates.chosen_complectation
            case 'color':
                state_to_set = AdminAdvertParametersStates.NewStateStates.chosen_color

        if state_to_set:
            await self.set_state(state, state_to_set)