import asyncio
import importlib
import logging
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.new_car_photo_requests import PhotoRequester
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__choose_state import \
    AdvertParametersChooseCarState
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_deletion.start_deletion import \
    ActionOfDeletionExistsAdvertParameter
from utils.lexicon_utils.logging_utils.logg_string_utils import get_user_name
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')


class ConfirmDeleteExistsAdvertParameter(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        memory_storage = await state.get_data()
        params_state_type_flag = memory_storage.get('params_type_flag')
        ic(params_state_type_flag)
        match params_state_type_flag:
            case 'new':
                selected_parameters = memory_storage.get('selected_parameters')
            case 'second_hand':
                selected_parameters = {
                    memory_storage.get('admin_chosen_advert_parameter'): memory_storage.get('current_advert_parameter')['id']
                }
            case _:#
                ic()
                await self.send_alert_answer(request, Lexicon_module.ADVERT_PARAMETERS_LEXICON['memory_was_forgotten'])
                return await AdvertParametersChooseCarState().callback_handler(request, state)

        exists_model = await ActionOfDeletionExistsAdvertParameter().check_on_exists_adverts_by_parameter(
            state, selected_parameters
        )
        if exists_model:
            await self.send_alert_answer(
                request,
                Lexicon_module.ADVERT_PARAMETERS_LEXICON['this_advert_parameter_dont_can_was_deleting']
            )

        else:
            logg_message = await get_user_name(selected_parameters)
            try:
                delete_query = await self.delete_query(request, state, selected_parameters)
                ic(delete_query)
                ic()
            except Exception as ex:
                delete_query = 'no'
                traceback.print_exc()
                logging.critical(f'|||Ошибка при удалении связки параметров(удаление конфигурации авто): {ex}')
            if delete_query == 'no':
                alert_message = Lexicon_module.ADMIN_LEXICON['action_non_actuality']
            else:
                admin_lexicon_module = importlib.import_module('utils.lexicon_utils.admin_lexicon.admin_lexicon')

                asyncio.create_task(self.logging_action(request, 'deleted_param', reason=logg_message))
                alert_message = admin_lexicon_module.captions['successfully']
            await self.send_alert_answer(request, alert_message)
        ic()
        await state.update_data(delete_params_flag=True)

        match params_state_type_flag:
            case 'new':
                admin_backward_command_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_backward_command')

                await admin_backward_command_module\
                    .backward_in_advert_parameters_interface(memory_storage.get('last_params_state'), request, state)
            case 'second_hand':
                output_specific_parameters_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters')
                await output_specific_parameters_module\
                    .OutputSpecificAdvertParameters().callback_handler(request, state)#

    async def delete_query(self, request, state, selected_params):
        memory_storage = await state.get_data()
        delete_query = None
        params_type_flag = memory_storage.get('params_type_flag')
        ic(params_type_flag)
        match params_type_flag:
            case 'new':
                delete_query = await self.delete_new_state_params(selected_params)
            case 'second_hand':
                for parameter_type_name, parameter_value_id in selected_params.items():
                    delete_query = await car_configs_module\
                        .CarConfigs.custom_action(
                        action='delete',
                        model_id=int(parameter_value_id),
                        mode=parameter_type_name
                    )
            case _:
                ic()
                await self.send_alert_answer(request, Lexicon_module.ADVERT_PARAMETERS_LEXICON['memory_was_forgotten'])
                return await AdvertParametersChooseCarState().callback_handler(request, state)

        return delete_query

    async def delete_new_state_params(self, selected_params):
        async def find_dependencies(selected_data):
            dependencies = {}
            photos = None

            async def delete_low_params(current_param):
                if current_param == 'color':
                    colors = await car_configs_module\
                        .CarConfigs.get_color_by_complectaiton(selected_data['complectation'])
                    ic(colors)
                    if len(colors) <= 1:
                        dependencies['complectation'] = {selected_data['complectation']}
                        await delete_low_params('complectation')

                elif current_param == 'complectation':
                    complectations = await car_configs_module\
                        .CarConfigs.get_complectations_by_model_and_engine(selected_data['model'])
                    # complectations_by_engine = await car_configs_module\
                    # .CarConfigs.get_complectations_by_model_and_engine(selected_data['model'],
                    #                                                                                    selected_data['engine'])
                    ic(complectations)
                    # if sorted({complectation.id for complectation in complectations}) \
                    #         == sorted({complectation_by_engine.id for complectation_by_engine in complectations_by_engine}):
                    if len(complectations) <= 1:
                        dependencies['model'] = {selected_data['model']}
                        await delete_low_params('model')
                elif current_param == 'model':
                    models = await car_configs_module\
                        .CarConfigs.get_models_by_brand_and_engine(selected_data['brand'])
                    models_by_brand = await car_configs_module\
                        .CarConfigs.get_models_by_brand_and_engine(selected_data['brand'],
                                                                                      selected_data['engine'])
                    # if sorted({model.id for model in models}) \
                    #         == sorted({model_by_brand.id for model_by_brand in models_by_brand}):
                    if len(models) <= 1:
                        if 'model' not in dependencies.keys():
                            dependencies['model'] = {selected_data['model']}
                        if 'brand' not in dependencies.keys():
                            dependencies['brand'] = {selected_data['brand']}

            if 'color' in selected_data:
                # dependencies['color'] = {selected_data['color']}
                photos = await PhotoRequester.find_photos_by_complectation_and_color(selected_data['complectation'],
                                                                                     selected_data['color'])
                await delete_low_params('color')

            # Если 'complectation' есть в selected_data, то нет необходимости искать зависимости
            elif 'complectation' in selected_data:
                dependencies['complectation'] = {selected_data['complectation']}
                photos = await PhotoRequester.find_photos_by_complectation_and_color(selected_data['complectation'])
                await delete_low_params('complectation')

            # Если 'model' есть в selected_data, ищем зависимые 'complectation'
            elif 'model' in selected_data:
                # dependencies['model'] = {[selected_data['model']]}
                complectations = await car_configs_module\
                    .CarConfigs.get_complectations_by_model_and_engine(selected_data['model'],
                                                                                         selected_data['engine'])
                dependencies['complectation'] = {comp.id for comp in complectations}
                photos = await PhotoRequester.find_photos_by_model_and_engine(selected_data['model'],
                                                                              selected_data['engine'])
                await delete_low_params('model')

            # Если 'brand' есть в selected_data, ищем зависимые 'model'
            elif 'brand' in selected_data:
                ic(dependencies)
                # delete_low_params = await delete_low_params('brand')
                models = await car_configs_module\
                    .CarConfigs.get_models_by_brand_and_engine(selected_data['brand'],
                                                                         selected_data['engine'])
                if models:
                    dependencies['complectation'] = set()
                    ic(dependencies)

                    for model in models:
                        complectations = await car_configs_module\
                            .CarConfigs.get_complectations_by_model_and_engine(model,
                                                                                                 selected_data['engine'])
                        ic(complectations)
                        if complectations:
                            dependencies['complectation'].update({complectation.id for complectation in complectations})
                            ic(dependencies)

                dependencies['model'] = {mod.id for mod in models}
                ic(dependencies)
                # other_models = await car_configs_module\
                # .CarConfigs.get_models_by_brand_and_engine(selected_data['brand'])
                await delete_low_params('model')
                ic(dependencies)

                photos = await PhotoRequester.find_photos_by_brand_and_engine(selected_data['brand'],
                                                                              selected_data['engine'])
            return dependencies, photos

        async def delete_data(dependencies, photo_dependencies):
            advert_feedbacks_requests_module = importlib.import_module(
                'database.data_requests.statistic_requests.advert_feedbacks_requests')

            ic(dependencies)
            # Удаление фотографий
            photo_ids = [photo.id for photo in photo_dependencies]
            if photo_ids:
                await PhotoRequester.delete_by_id(photo_ids)

            # Удаление зависимостей
            params_can_delete = ['color', 'complectation', 'model', 'brand']
            for table_name in params_can_delete:
                if table_name in dependencies.keys():
                    ic(table_name)
                    await advert_feedbacks_requests_module\
                            .AdvertFeedbackRequester.update_parameters_to_null_by_specific_parameter(table_name,
                                                                                                  dependencies[table_name])
                    if table_name != 'color':
                        await car_configs_module\
                            .CarConfigs.custom_action(table_name, 'delete', model_id=dependencies[table_name])

        if 'state' in selected_params:
            selected_params.pop('state')

        ic(selected_params)
        params_to_delete, photo_dependencies = await find_dependencies(selected_params)
        ic(params_to_delete, photo_dependencies)
        # photo_dependencies = await find_photo_dependencies(data_to_delete)
        # ic(photo_dependencies)
        delete_query = await delete_data(params_to_delete, photo_dependencies)
        return delete_query