import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from database.data_requests.new_car_photo_requests import PhotoRequester
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.choose_catalog_action import \
    choose_catalog_action_admin_handler
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from utils.translator import translate

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


class ConfirmLoadNewParamsBranchHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # insert_query_flag = await self.this_branch_is_exists()
        insert_query = await self.insert_new_branch(request, state, request.from_user.id)
        if insert_query == 'exit':
            self.output_methods = []
            return
        if insert_query:
            admin_lexicon_module = importlib.import_module('utils.lexicon_utils.admin_lexicon.admin_lexicon')

            await self.send_alert_answer(request, admin_lexicon_module.captions['successfully'], message=True)
        else:

            await self.send_alert_answer(request, Lexicon_module.ADMIN_LEXICON['action_non_actuality'],
                                         message=True)

        await choose_catalog_action_admin_handler(request, state)

    async def insert_new_branch(self, request, state: FSMContext, admin_id):
        current_branch_exists = await self.exists_branch(state)
        if current_branch_exists:
            await self.send_alert_answer(request, Lexicon_module.ADMIN_LEXICON['branch_is_exists'])
            await choose_catalog_action_admin_handler(request, state)
            return 'exit'
        param_objects = await self.get_selected_param_models(state)
        insert_query = None
        current_state = await self.get_state_string(state)
        ic(current_state)
        # if not param_objects.get('color'):
        #     from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.change_state.confirm import \
        #         ConfirmChangeStateOnExistsBranchHandler
        #     await ConfirmChangeStateOnExistsBranchHandler().callback_handler(request, state)
        #     return 'exit'
        memory_storage = await state.get_data()
        selected_params = memory_storage.get('selected_parameters')
        ic()
        ic(selected_params, str(selected_params.get('state')), param_objects)
        # if str(selected_params.get('state')) != '2':
        if memory_storage.get('change_state_flag') and str(selected_params.get('state')) == '2':

            car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')
            param_objects['engine'] = selected_params['engine']
            ic(param_objects) # есть тут стейт?
            from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_deletion.start_deletion import \
                ActionOfDeletionExistsAdvertParameter
            exists_adverts = await ActionOfDeletionExistsAdvertParameter().check_on_exists_adverts_by_parameter(
                state, param_objects
            )
            ic(exists_adverts)
            if not exists_adverts:
                ic(memory_storage.get('change_state_flag'))
                if memory_storage.get('change_state_flag'):
                    new_state = memory_storage.get('new_state')
                    actual_complectation_id = await car_configs_module.CarConfigs.update_complectation_wired_state(
                        param_objects['complectation'].id,
                        param_objects['color'].id if hasattr(param_objects['color'], 'id') else None,
                        new_state,
                        selected_params['state']
                    )
                    # if insert_query:
                    #     change_state_flag = memory_storage.get('change_state_flag')
                    #     if change_state_flag == 'from_used':
                    ic(actual_complectation_id)
                    if actual_complectation_id:
                        actual_complectation_id = actual_complectation_id[0][0]
                        param_objects['complectation'] = actual_complectation_id

                        # ic(insert_query)
                        # if insert_query:
                        await state.update_data(change_state_flag=None)
                    else:
                        return False
        # else:
        #     param_objects['complectation'] = param_objects['complectation'].id
        if selected_params.get('photos') and param_objects.get('color'):
            insert_query = await PhotoRequester.insert_photos_in_param_branch(selected_params.get('photos'),
                                                                              param_objects['color'],
                                                                              param_objects['complectation'],
                                                                              admin_id)
        else:
            insert_query = True
        if insert_query:
            asyncio.create_task(self.logging_action(request, state, param_objects))
        else:
            raise Exception()
        ic(insert_query)
        return insert_query

    async def exists_branch(self, state: FSMContext, rewriting_complectation = False):
        from database.data_requests.car_configurations_requests import CarConfigs
        ic()
        # return False
        memory_storage = await state.get_data()
        selected_parameters = memory_storage.get('selected_parameters')
        ic(selected_parameters)
        state_value = str(selected_parameters['state'])

        exists_params = {}
        default_params = ['brand', 'model', 'color']#, 'model', 'complectation', 'color']
        for key in default_params:
            value = selected_parameters.get(key)
            ic(key, value)
            if isinstance(value, dict):
                value = value['added']

                match key:
                    case 'model':

                        value = await CarConfigs.get_model_by_brand_and_name(
                            exists_params['brand'],
                            value)
                    case _:
                        value = await CarConfigs.custom_action(key, name=value, action='get_by_name')
                if not value:
                    if key == 'color' and state_value != 1:
                        pass
                    else:
                        return
            exists_params[key] = value
        exists_params['engine'] = selected_parameters['engine']
        ic(selected_parameters['state'])
        if isinstance(selected_parameters['complectation'], dict) or rewriting_complectation:
            if rewriting_complectation:
                selected_parameters['complectation'] = {'added': rewriting_complectation}
            exists_params['complectation'] = await translate.translate(selected_parameters['complectation']['added'],
                                                                       'name')
        else:
            # return
            complectation = await CarConfigs.get_by_id('complectation', selected_parameters['complectation'])
            if complectation:
                if complectation._name:
                    exists_params['complectation'] = {'_name': complectation._name}
                else:
                    exists_params['complectation'] = {'name_ru': complectation.name_ru, 'name_uz': complectation.name_uz}
            else:

                ic()
                return
            bind_exists = await CarConfigs.get_branch(exists_params)
            ic(bind_exists)
            ic()
            return bind_exists

        ic(exists_params['complectation'])
        ic(state_value)
        #
        # if all(exists_params.get(param_name) for param_name in ('complectation', 'color')):
        #
        #     bind_exists = await PhotoRequester.find_photos_by_complectation_and_color(exists_params['complectation'],
        #                                                                               exists_params['color'])
        bind_exists = None
        if state_value != '1':
            ic()
            bind_exists = await CarConfigs.get_complectations_by_model_and_engine_and_state(exists_params['model'],
                                                                                            2,
                                                                                            name=exists_params[
                                                                                                'complectation'
                                                                                            ])

            # if not bind_exists:
            #     bind_exists = await CarConfigs.get_complectations_by_model_and_engine_and_state(exists_params['model'],
            #                                                                                     None,
            #                                                                                     name=exists_params[
            #                                                                                         'complectation'
            #                                                                                     ])
            ic(bind_exists)
            ic((exists_params['model'], 2,
                                                                                            exists_params[
                                                                                                'complectation'
                                                                                            ]))
        if not bind_exists and state_value != '2':
            ic()
            bind_exists = await CarConfigs.get_branch(exists_params)
        ic(bind_exists)
        if bind_exists:
            return True

    async def get_selected_param_models(self, state: FSMContext):
        car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')

        memory_storage = await state.get_data()
        selected_parameters = memory_storage.get('selected_parameters')
        ic(selected_parameters)
        ic()
        good_params = {}
        default_params = ['brand', 'model', 'complectation', 'color']
        for key in default_params:
            value = selected_parameters.get(key)

            ic(key, value)
            if isinstance(value, dict):
                value = value['added']
                if key == 'color':
                    current_param = await self.get_selected_color(value)
                    ic(current_param, value)
                else:
                    if key == 'model':
                        subtables = {'first_subject': good_params['brand']}
                    elif key == 'complectation':
                        subtables = {'first_subject': good_params['model'],
                                     'second_subject': selected_parameters['engine_type' if 'engine_type' in selected_parameters.keys()
                                                                                 else 'engine'],
                                     'third_subject': selected_parameters['state']}
                    else:
                        subtables = {}
                    # if key == 'brand':
                    if key in ('brand', 'model', 'complectation'):

                        action = 'insert_or_get'
                    else:
                        action = 'insert'
                    current_param = await car_configs_module\
                        .CarConfigs.custom_action(key, action, value, **subtables)
                    if action == 'insert_or_get' and isinstance(current_param, tuple):
                        current_param = current_param[0]
            else:
                current_param = await car_configs_module\
                    .CarConfigs.get_by_id(key, value)

            if current_param == '(translate_error)':
                current_param = value
            good_params[key] = current_param
            ic(good_params)
        ic(good_params)
        return good_params

    async def get_selected_color(self, color):
        car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')

        color_exists = await car_configs_module\
            .CarConfigs.get_or_add_color(color)

        return color_exists


    async def logging_action(self, request, state, param_objects):
        memory_storage = await state.get_data()
        add_new_branch_status = memory_storage.get('add_new_branch_status')
        if not add_new_branch_status:
            logging_action = 'rebooted_param_branch_photo'
        else:
            logging_action = 'add_param_branch'

        await log_admin_action(request.from_user.username, logging_action, subject=param_objects)
