import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.new_car_photo_requests import PhotoRequester
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.choose_catalog_action import \
    choose_catalog_action_admin_handler
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler



class ConfirmLoadNewParamsBranchHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        insert_query = await self.insert_new_branch(request, state, request.from_user.id)
        if insert_query:
            admin_lexicon_module = importlib.import_module('utils.lexicon_utils.admin_lexicon.admin_lexicon')

            await self.send_alert_answer(request, admin_lexicon_module.captions['successfully'])
            await choose_catalog_action_admin_handler(request, state)
        else:
            Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

            await self.send_alert_answer(request, Lexicon_module.ADMIN_LEXICON['action_non_actuality'])

    # async def update_branch_photos(self, state: FSMContext):
    #     memory_storage = await state.get_data()
    #     selected_params = memory_storage.get('selected_parameters')
    #     update_query = await PhotoRequester.update_adverts_photos()

    async def insert_new_branch(self, request, state: FSMContext, admin_id):
        memory_storage = await state.get_data()
        selected_params = memory_storage.get('selected_parameters')
        param_objects = await self.get_selected_param_models(state)
        insert_query = await PhotoRequester.insert_photos_in_param_branch(selected_params.get('photos'),
                                                                          param_objects['color'],
                                                                          param_objects['complectation'],
                                                                          admin_id)
        if insert_query:
            asyncio.create_task(self.logging_action(request, state, param_objects))
        ic(insert_query)
        return insert_query

    async def get_selected_param_models(self, state: FSMContext):
        memory_storage = await state.get_data()
        selected_parameters = memory_storage.get('selected_parameters')
        ic(selected_parameters)
        ic()
        good_params = {}
        for key, value in selected_parameters.items():
            if key == 'photos':
                # good_params[key] = value
                continue

            ic(key, value)
            if isinstance(value, dict):
                value = value['added']
                if key == 'color':
                    current_param = await self.get_selected_color(value)
                    current_param = current_param[0]
                else:
                    if key == 'model':
                        subtables = {'first_subject': good_params['brand']}
                    elif key == 'complectation':
                        subtables = {'first_subject': good_params['model'],
                                     'second_subject': good_params['engine_type']}
                    else:
                        subtables = {}
                    current_param = await CarConfigs.custom_action(value, 'insert', value, **subtables)
            else:
                current_param = await CarConfigs.get_by_id(key, value)

            good_params[key] = current_param
        ic(good_params)
        return good_params

    async def get_selected_color(self, color):
        color_exists = await CarConfigs.get_or_add_color(color)

        return color_exists


    async def logging_action(self, request, state, param_objects):
        memory_storage = await state.get_data()
        add_new_branch_status = memory_storage.get('add_new_branch_status')
        if not add_new_branch_status:
            logging_action = 'rebooted_param_branch_photo'
        else:
            logging_action = 'add_param_branch'

        await log_admin_action(request.from_user.username, logging_action, subject=param_objects)
