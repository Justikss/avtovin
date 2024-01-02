from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.data_requests.car_configurations_requests import CarConfigs
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.utils.add_new_value_advert_parameter\
    .add_new_value_advert_parameter import AddNewValueAdvertParameter
from utils.oop_handlers_engineering.update_handlers.base_objects.base_filter import BaseFilterObject


class AdvertParameterValueFilter(BaseFilterObject):
    async def __call__(self, message: Message, state: FSMContext,
                       incorrect_flag=None,
                       message_input_request_handler=AddNewValueAdvertParameter().callback_handler) -> bool:
        memory_storage = await state.get_data()
        last_advert_parameter = memory_storage.get('admin_chosen_advert_parameter')
        ic(last_advert_parameter)
        if last_advert_parameter in ('mileage', 'year', 'color', 'brand'):
            existing_value = await CarConfigs.get_or_insert(last_advert_parameter, 'get_by_name', name=message.text)
            ic(existing_value)
            if existing_value:
                incorrect_flag = '(exists)'
        else:
            pass #допилить
        ic(incorrect_flag)
        return await super().__call__(message, state, incorrect_flag=incorrect_flag,
                                      message_input_request_handler=message_input_request_handler)
