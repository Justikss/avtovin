import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.add_new_value_advert_parameter.add_new_value_advert_parameter import \
    AddNewValueAdvertParameter
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class ConfirmAddNewValueOfAdvertParameter(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        memory_storage = await state.get_data()
        insert_query = None
        param_kwarg = None
        match memory_storage.get('params_type_flag'):

            case 'new':
                selected_param_name = memory_storage.get('next_params_output')
                selected_parameters = memory_storage.get('selected_parameters')
                param_kwarg = None
                selected_parameters[selected_param_name] = {'added': memory_storage.get('current_value')}
                await self.try_set_add_new_params_branch_status(state, selected_param_name)
                ic(await state.update_data(selected_parameters=selected_parameters))
                second_hand_mode_output = await self.set_next_param_to_choose(request, state, memory_storage)
                # second_hand_mode_output = await self.set_next_param_to_choose(request, state, memory_storage)
                # if second_hand_mode_output:
                #     from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_params_branch_review import \
                #         ParamsBranchReviewHandler
                #     await ParamsBranchReviewHandler().callback_handler(request, state, second_hand_mode=True, make_output=True)
                #     return
            case 'second_hand':
                car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')

                param_kwarg = {memory_storage.get('admin_chosen_advert_parameter'): memory_storage.get('current_value')}
                insert_query = await car_configs_module\
                    .CarConfigs.custom_action(mode=memory_storage.get('admin_chosen_advert_parameter'),
                                               name=memory_storage.get('current_value'),
                                               action='insert')
        if insert_query == '(exists)':
            await AddNewValueAdvertParameter().callback_handler(request, state, incorrect=insert_query)
            await super().process_callback(request, state, **kwargs)
        else:
            admin_lexicon_module = importlib.import_module('utils.lexicon_utils.admin_lexicon.admin_lexicon')
            output_specific_parameters_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters')
            if not memory_storage.get('params_type_flag') == 'new':
                await self.send_alert_answer(request, admin_lexicon_module.captions['successfully'], message=True)
            ic(insert_query)
            ic()
            await output_specific_parameters_module.OutputSpecificAdvertParameters().callback_handler(request, state)#
            if param_kwarg:
                asyncio.create_task(self.logging_action(request, 'added_param', param_kwarg))


    async def set_next_param_to_choose(self, request: Message | CallbackQuery, state: FSMContext, memory_storage: dict):
        output_specific_parameters_module = importlib.import_module(
            'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters')

        next_params_output = None
        last_params_to_output = memory_storage.get('next_params_output')
        # return await ParamsBranchReviewHandler().process_callback(request, state)

        if last_params_to_output == 'color' and \
                await output_specific_parameters_module.OutputSpecificAdvertParameters().check_state_on_add_new_branch_status(state):
            next_params_output = 'photo'
        else:

            ic(last_params_to_output)
            parameter_names = ['state', 'engine', 'brand', 'model', 'complectation', 'color']
            if await output_specific_parameters_module.OutputSpecificAdvertParameters().check_state_on_add_new_branch_status(state):
                try:
                    selected_parameters = memory_storage.get('selected_parameters')

                    # if str(selected_parameters.get('state')) == '2':
                    #     return True
                    # else:
                    # Получаем индекс последнего выбранного элемента и пытаемся взять следующий элемент
                    next_params_output = next(
                        iter(parameter_names[parameter_names.index(last_params_to_output) + 1:]), None)
                    ic()
                    ic(next_params_output)
                except ValueError:
                    # Если last_chosen не найден в списке, обрабатываем ошибку
                    next_params_output = None
        ic(next_params_output)
        await state.update_data(next_params_output=next_params_output)

    async def try_set_add_new_params_branch_status(self, state: FSMContext, status_to_set: str):
        memory_storage = await state.get_data()
        ic()
        ic(memory_storage.get('params_type_flag'))
        ic(memory_storage.get('can_set_add_new_branch_status'))
        change_state_flag = memory_storage.get('change_state_flag')
        if not change_state_flag:
            if memory_storage.get('params_type_flag') == 'new':
                if memory_storage.get('can_set_add_new_branch_status'):
                    await state.update_data(add_new_branch_status=status_to_set)

