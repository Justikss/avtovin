from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.car_configurations_requests import CarConfigs
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__choose_state import \
    AdvertParametersChooseCarState
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters import \
    OutputSpecificAdvertParameters
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.utils.add_new_value_advert_parameter\
    .add_new_value_advert_parameter import AddNewValueAdvertParameter
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.utils.handling_exists_value_advert_parameter.action_of_rewriting.start_rewrite_exsits_advert_parameter import \
    RewriteExistsAdvertParameterHandler
from handlers.utils.message_answer_without_callback import send_message_answer
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.custom_exceptions.database_exceptions import FilterWithoutInput
from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON
from utils.oop_handlers_engineering.update_handlers.base_objects.base_filter import BaseFilterObject


class AdvertParameterValueFilter(BaseFilterObject):
    async def __call__(self, request: Message | CallbackQuery, state: FSMContext,
                       incorrect_flag=None,
                       message_input_request_handler=None) -> bool:

        message_input_request_handler = await self.get_returning_method(request, state)
        memory_storage = await state.get_data()
        ic(str(await state.get_state()))

        if isinstance(request, Message):
            inputted_value = request.text
        elif await state.get_state() == AdminAdvertParametersStates.confirmation_rewrite_exists_parameter:
            inputted_value = memory_storage.get('current_new_parameter_value')
        else:
            raise FilterWithoutInput()
        last_advert_parameter = memory_storage.get('admin_chosen_advert_parameter')
        ic(last_advert_parameter)

        if last_advert_parameter in ('mileage', 'year'):
            existing_value = await CarConfigs.custom_action(last_advert_parameter, 'get_by_name', name=inputted_value)
        else:
            existing_value = await self.seek_matched_new_state_param_names(request, state, last_advert_parameter,
                                                                           inputted_value)

        ic(existing_value)
        if existing_value:
            incorrect_flag = '(exists)'
        ic(incorrect_flag)
        return await super().__call__(request, state, incorrect_flag=incorrect_flag,
                                      message_input_request_handler=message_input_request_handler)

    @staticmethod
    async def get_returning_method(request, state):
        current_state = str(await state.get_state())
        match current_state:
            case 'AdminAdvertParametersStates:start_add_value_process':
                message_input_request_handler = AddNewValueAdvertParameter().callback_handler
            case 'AdminAdvertParametersStates:start_rewrite_exists_parameter' | 'AdminAdvertParametersStates:confirmation_rewrite_exists_parameter':
                message_input_request_handler = RewriteExistsAdvertParameterHandler().callback_handler
            case _:#
                await send_message_answer(request, ADVERT_PARAMETERS_LEXICON['memory_was_forgotten'])
                return await AdvertParametersChooseCarState().callback_handler(request, state)

        return message_input_request_handler

    async def seek_matched_new_state_param_names(self, request, state: FSMContext, last_advert_parameter, parameter_value):
        current_params = await OutputSpecificAdvertParameters().get_need_new_car_state_params(request,
                                                                                              state, last_advert_parameter)
        if current_params:
            current_names = [param.name for param in current_params]
            if parameter_value in current_names:
                return True

