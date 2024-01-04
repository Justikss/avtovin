import logging
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.recomendations_request import RecommendationParametersBinder
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
        parameter_type_name = memory_storage.get('admin_chosen_advert_parameter')
        parameter_value_id = memory_storage.get('current_advert_parameter')['id']
        # parameter_value_name = memory_storage.get('current_advert_parameter')['value']
        exists_model = await ActionOfDeletionExistsAdvertParameter().check_on_exists_adverts_by_parameter(
            state, parameter_type_name, parameter_value_id
        )
        if exists_model:
            await self.send_alert_answer(
                request,
                ADVERT_PARAMETERS_LEXICON['this_advert_parameter_dont_can_was_deleting']
            )

        else:
            try:
                delete_query = await CarConfigs.custom_action(
                    action='delete',
                    model_id=int(parameter_value_id),
                    mode=parameter_type_name
                )
                ic(delete_query)
            except Exception as ex:
                traceback.print_exc()
                logging.critical(f'|||Ошибка при удалении связки параметров(удаление конфигурации авто): {ex}')

            await self.send_alert_answer(request,
                                         captions['successfully'])
        ic()
        return await OutputSpecificAdvertParameters().callback_handler(request, state)#