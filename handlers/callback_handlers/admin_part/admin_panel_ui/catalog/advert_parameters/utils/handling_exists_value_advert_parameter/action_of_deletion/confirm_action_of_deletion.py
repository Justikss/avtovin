import logging
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.new_car_photo_requests import PhotoRequester
from database.data_requests.recomendations_request import RecommendationParametersBinder
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__choose_state import \
    AdvertParametersChooseCarState
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters import \
    OutputSpecificAdvertParameters
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.utils.handling_exists_value_advert_parameter.action_of_deletion.start_action_of_deletion import \
    ActionOfDeletionExistsAdvertParameter
from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON
from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler


class ConfirmDeleteExistsAdvertParameter(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        memory_storage = await state.get_data()
        match memory_storage.get('params_type_flag'):
            case 'new':
                selected_parameters = memory_storage.get('selected_parameters')
            case 'second_hand':
                selected_parameters = {
                    memory_storage.get('admin_chosen_advert_parameter'): memory_storage.get('current_advert_parameter')['id']
                }
            case _:#
                await self.send_alert_answer(request, ADVERT_PARAMETERS_LEXICON['memory_was_forgotten'])
                return await AdvertParametersChooseCarState().callback_handler(request, state)

        exists_model = await ActionOfDeletionExistsAdvertParameter().check_on_exists_adverts_by_parameter(
            state, selected_parameters
        )
        if exists_model:
            await self.send_alert_answer(
                request,
                ADVERT_PARAMETERS_LEXICON['this_advert_parameter_dont_can_was_deleting']
            )

        else:

            try:
                delete_query = await self.delete_query(request, state, selected_parameters)
                ic(delete_query)
            except Exception as ex:
                traceback.print_exc()
                logging.critical(f'|||Ошибка при удалении связки параметров(удаление конфигурации авто): {ex}')

            await self.send_alert_answer(request,
                                         captions['successfully'])
        ic()
        return await OutputSpecificAdvertParameters().callback_handler(request, state)#

    async def delete_query(self, request, state, selected_params):
        memory_storage = await state.get_data()
        delete_query = None

        match memory_storage.get('params_type_flag'):
            case 'new':
                delete_query = await self.delete_new_state_params(selected_params)
            case 'second_hand':
                for parameter_type_name, parameter_value_id in selected_params.items():
                    delete_query = await CarConfigs.custom_action(
                        action='delete',
                        model_id=int(parameter_value_id),
                        mode=parameter_type_name
                    )
            case _:
                await self.send_alert_answer(request, ADVERT_PARAMETERS_LEXICON['memory_was_forgotten'])
                return await AdvertParametersChooseCarState().callback_handler(request, state)

        return delete_query

    async def delete_new_state_params(self, selected_params):
        async def find_dependencies(selected_data):
            dependencies = {}
            last_key = list(selected_data.keys())[-1]

            # Функция для добавления зависимостей
            async def add_dependency(dep_key, getter_func, *args):
                items = await getter_func(*args)
                dependencies[dep_key] = [item.id for item in items]

            # Словарь сопоставления ключей и функций для получения зависимостей
            dependency_getters = {
                'model': (add_dependency, 'complectation', CarConfigs.get_complectations_by_model_and_engine,
                          selected_data.get('model')),
                'brand': (
                add_dependency, 'model', CarConfigs.get_models_by_brand_and_engine, selected_data.get('brand')),
            }

            # Выполнение функции добавления зависимостей, если это необходимо
            if last_key in dependency_getters:
                func, dep_key, getter, arg = dependency_getters[last_key]
                await func(dep_key, getter, arg)

            return dependencies

        async def find_photo_dependencies(last_key, last_value):
            photo_dependencies = []

            if last_key == 'complectation':
                photos = await PhotoRequester.find_photos_by_complectation(last_value)
                photo_dependencies.extend(photos)
            elif last_key == 'model':
                photos = await PhotoRequester.find_photos_by_model(last_value)
                photo_dependencies.extend(photos)
            elif last_key == 'brand':
                photos = await PhotoRequester.find_photos_by_brand(last_value)
                photo_dependencies.extend(photos)

            return photo_dependencies

        async def delete_data(params, dependencies, photo_dependencies):
            # Удаляем зависимости
            for table, ids in dependencies.items():
                for param_id in ids:
                    await CarConfigs.custom_action(table, 'delete', model_id=param_id)

            # Удаляем фотографии
            for photo in photo_dependencies:
                await CarConfigs.custom_action('new_car_photo', 'delete', model_id=photo.id)

            # Удаляем основные параметры
            for table in reversed(list(params.keys())):
                await CarConfigs.custom_action(table, 'delete', model_id=params[table])

        data_to_delete = await find_dependencies(selected_params)
        ic(data_to_delete)
        photo_dependencies = await find_photo_dependencies(list(selected_params.keys())[-1],
                                                           list(selected_params.values())[-1])
        ic(photo_dependencies)
        delete_query = await delete_data(selected_params, data_to_delete, photo_dependencies)
        return delete_query