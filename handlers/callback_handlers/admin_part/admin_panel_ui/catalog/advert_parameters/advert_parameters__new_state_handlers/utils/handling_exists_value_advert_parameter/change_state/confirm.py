import importlib
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class ConfirmChangeStateOnExistsBranchHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):

        if request.data.startswith('change_state:'):
            new_state_value = request.data.split(':')[-1]
        # else:
        #     selected_parameters = await self.get_from_memory_storage(state, 'selected_parameters')
        #     new_state_value = selected_parameters['state']
            if new_state_value == 'none':
                new_state_value = None

            update_state = await self.handle_confirm(request, state, new_state_value)

            await self.handler_return(request, state, update_state)

    async def handler_return(self, request, state, update_state):
        ic(update_state)
        match update_state:
            case 'successfully':
                from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.choose_car_state import \
                    ChooseStateAddNewParamsHandler
                await state.clear()
                await ChooseStateAddNewParamsHandler().callback_handler(request, state)
            case 'unsuccessfully':
                ic()
                print('ParamsBranchReviewHandler()cbh')
                from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_params_branch_review import \
                    ParamsBranchReviewHandler
                await ParamsBranchReviewHandler().callback_handler(request, state, make_output=True)

    async def handle_confirm(self, request: Message | CallbackQuery, state: FSMContext, new_state_value):

        memory_storage = await state.get_data()
        selected_params = memory_storage.get('selected_parameters')
        current_state = str(await state.get_state())
        ic()
        ic(current_state, selected_params)
        old_state = selected_params['state']
        color_exists = selected_params.get('color')
        ic(current_state)
        ic(selected_params.get('state'), new_state_value)
        if not memory_storage.get('change_state_flag'):
            ic(await state.update_data(old_state=old_state))
        if current_state in ('AdminAdvertParametersStates.NewStateStates:parameters_branch_review',
                               'AdminAdvertParametersStates.NewStateStates:await_input_change_state_photos'):
            from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_deletion.start_deletion import \
                ActionOfDeletionExistsAdvertParameter
            exists_adverts = await ActionOfDeletionExistsAdvertParameter().check_on_exists_adverts_by_parameter(
                state, selected_params
            )
            ic()
            ic(exists_adverts)
            if exists_adverts:
                await self.send_alert_answer(request,
                                             self.lexicon_module.ADVERT_PARAMETERS_LEXICON['state_update_impossible'],
                                             message=True)
                return False


        if str(new_state_value) == '2':
            if selected_params.get('photos'):
                del selected_params['photos']
            if selected_params.get('color'):
                del selected_params['color']
        if str(selected_params['state']) == '1' and not memory_storage.get('change_state_flag'):
            ic()
            car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')
            ic(new_state_value)
            update_query = await car_configs_module.CarConfigs.update_complectation_wired_state(
                selected_params['complectation'], selected_params.get('color') or color_exists, new_state_value,
                selected_params['state']
            )
            ic(update_query)
            if update_query:
                alert_text_key = 'successfully'

            else:
                alert_text_key = 'unsuccessfully'

            from utils.lexicon_utils.Lexicon import ADMIN_LEXICON
            await self.send_alert_answer(request, ADMIN_LEXICON[alert_text_key], message=True)
            return alert_text_key
        if current_state == 'AdminAdvertParametersStates.NewStateStates:confirmation_new_params_branch_to_load':
            # review_mode = 'load'
            ic()
            ic(selected_params.get('state'), new_state_value)
            # ic(await state.update_data(old_state=selected_params.get('state')))

            if selected_params.get('state') == '2' and str(new_state_value) != '2':
                from_used = 'from_used'
                if any(isinstance(value, dict) for value in selected_params.values()):
                    from_used = 'from_used_add'
            else:
                from_used = False

            if (memory_storage.get('change_state_flag') and ic(str(memory_storage.get('old_state'))) != str(new_state_value)) or not memory_storage.get('change_state_flag'):
                await state.update_data(change_state_flag=from_used if from_used else True)
                await state.update_data(new_state=new_state_value)
            else:
                await state.update_data(change_state_flag=None)
                await state.update_data(new_state=None)
                ic(await state.update_data(old_state=None))
            selected_params['state'] = new_state_value

            await state.update_data(selected_parameters=selected_params)
            ic(from_used)
            if from_used and str(new_state_value) != '2':
                from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters import \
                    OutputSpecificAdvertParameters
                await state.update_data(next_params_output='color')
                return await OutputSpecificAdvertParameters().callback_handler(request, state)
            # await self.send_alert_answer(request, captions['successfully'], message=True)
            from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_params_branch_review import \
                ParamsBranchReviewHandler
            ic()
            print('ParamsBranchReviewHandler()cbh')
            ic(memory_storage.get('add_new_branch_status'), not selected_params.get('state') == '2' and str(new_state_value) != '2')
            await ParamsBranchReviewHandler().callback_handler(request, state,
                                                               media_photos=selected_params.get('photos'),
                                                               make_output=True,
                                                               second_hand_mode='add' if not selected_params.get('state') == '2' and str(new_state_value) != '2'
                                                                                        else 'second_hand_review' if not memory_storage.get('add_new_branch_status')
                                                                                                                  else 'add' if not memory_storage.get('change_state_flag') else True)
        elif current_state in ('AdminAdvertParametersStates.NewStateStates:parameters_branch_review',
                               'AdminAdvertParametersStates.NewStateStates:await_input_change_state_photos') or not color_exists:

            ic(old_state, str(new_state_value))
            # traceback.print_stack()
            if str(old_state) == '2':
                await state.update_data(next_params_output='color')
                # await state.update_data(old_state=selected_params['state'])
                # selected_params['state'] = new_state_value
                await state.update_data(new_state=new_state_value)
                if any(isinstance(value, dict) for value in selected_params.values()):
                    change_state_flag = 'from_used_add'
                else:
                    change_state_flag = 'from_used'
                await state.update_data(change_state_flag=change_state_flag)
                from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.add_new_value_advert_parameter.add_new_value_advert_parameter import \
                    AddNewValueAdvertParameter
                await AddNewValueAdvertParameter().callback_handler(request, state)
                # from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters import \
                #     OutputSpecificAdvertParameters
                # await OutputSpecificAdvertParameters().callback_handler(request, state)
                # from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.add_new_value_advert_parameter.input_media_group_to_advert.input_media import \
                #     InputCarPhotosToSetParametersBranchHandler
                # await InputCarPhotosToSetParametersBranchHandler().callback_handler(request, state,
                #                                                                     update_state_mode=True)

                return
            elif str(new_state_value) == '2':
                # await state.update_data(new_state=new_state_value)
                # await state.update_data(change_state_flag='from_used')
                from database.data_requests.new_car_photo_requests import PhotoRequester
                # await PhotoRequester.delete_by_color_and_complectation(selected_params['complectation'],
                #                                                        selected_params['color'])


        else:
            raise ValueError(f'State {await state.get_state()} is not in (AdminAdvertParametersStates.NewStateStates:confirmation_new_params_branch_to_load, AdminAdvertParametersStates.NewStateStates:parameters_branch_review)')
        # return review_mode
