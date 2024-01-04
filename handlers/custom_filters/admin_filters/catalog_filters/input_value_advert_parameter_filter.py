from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.car_configurations_requests import CarConfigs
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.utils.add_new_value_advert_parameter\
    .add_new_value_advert_parameter import AddNewValueAdvertParameter
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.utils.handling_exists_value_advert_parameter.action_of_rewriting.start_rewrite_exsits_advert_parameter import \
    RewriteExistsAdvertParameterHandler
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.custom_exceptions.database_exceptions import FilterWithoutInput
from utils.oop_handlers_engineering.update_handlers.base_objects.base_filter import BaseFilterObject


class AdvertParameterValueFilter(BaseFilterObject):
    async def __call__(self, request: Message | CallbackQuery, state: FSMContext,
                       incorrect_flag=None,
                       message_input_request_handler=None) -> bool:

        message_input_request_handler = await self.get_returning_method(state)
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
            ic(existing_value)
            if existing_value:
                incorrect_flag = '(exists)'
        else:
            pass #допилить под new car state branches
        ic(incorrect_flag)
        return await super().__call__(request, state, incorrect_flag=incorrect_flag,
                                      message_input_request_handler=message_input_request_handler)

    @staticmethod
    async def get_returning_method(state):
        current_state = str(await state.get_state())
        match current_state:
            case 'AdminAdvertParametersStates:start_add_value_process':
                message_input_request_handler = AddNewValueAdvertParameter().callback_handler
            case 'AdminAdvertParametersStates:start_rewrite_exists_parameter' | 'AdminAdvertParametersStates:confirmation_rewrite_exists_parameter':
                message_input_request_handler = RewriteExistsAdvertParameterHandler().callback_handler
            case _:
                return

        return message_input_request_handler

    #
    # async def check_on_exists_new_state_param_names(self, current_advert_parameter):
    #
    #
    #     match current_advert_parameter:
    #
    #         pass