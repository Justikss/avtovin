import importlib
import re
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__choose_state import \
    AdvertParametersChooseCarState
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.add_new_value_advert_parameter.add_new_value_advert_parameter import AddNewValueAdvertParameter
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_rewriting.start import \
    RewriteExistsAdvertParameterHandler

from handlers.utils.message_answer_without_callback import send_message_answer
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.custom_exceptions.database_exceptions import FilterWithoutInput
from utils.oop_handlers_engineering.update_handlers.base_objects.base_filter import BaseFilterObject


class AdvertParameterValueFilter(BaseFilterObject):
    async def __call__(self, request: Message | CallbackQuery, state: FSMContext,
                       incorrect_flag=None,
                       message_input_request_handler=None) -> bool:
        config_module = importlib.import_module('config_data.config')

        message_input_request_handler = await self.get_returning_method(request, state)
        memory_storage = await state.get_data()
        ic(str(await state.get_state()))

        if isinstance(request, Message):
            inputted_value = request.text.strip()
        elif await state.get_state() == AdminAdvertParametersStates.confirmation_rewrite_exists_parameter:
            inputted_value = memory_storage.get('current_new_parameter_value')
        else:
            raise FilterWithoutInput()
        if memory_storage.get('params_type_flag') == 'new':
            last_advert_parameter = memory_storage.get('next_params_output')
        else:
            last_advert_parameter = memory_storage.get('admin_chosen_advert_parameter')
        ic(last_advert_parameter)

        incorrect_flag = await self.used_car_parameters_validator(last_advert_parameter, inputted_value)
        if not incorrect_flag:
            from config_data.config import max_advert_parameter_name_len
            if len(inputted_value) > max_advert_parameter_name_len:
                incorrect_flag = '(len)'

        else:
            if last_advert_parameter in ('mileage', 'year'):
                car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')

                existing_value = await car_configs_module.CarConfigs.custom_action(last_advert_parameter, 'get_by_name',
                                                                                   name=inputted_value)
            else:
                existing_value = await self.seek_matched_new_state_param_names(request, state, last_advert_parameter,
                                                                               inputted_value)

            ic(existing_value)
            if existing_value:
                incorrect_flag = '(exists)'
        if not incorrect_flag:
            incorrect_flag = await self.default_parameters_validator(last_advert_parameter, inputted_value)

        ic(incorrect_flag)
        return await super().__call__(request, state, incorrect_flag=incorrect_flag,
                                      message_input_request_handler=message_input_request_handler)

    async def default_parameters_validator(self, parameter_name, inputted_value):
        async def is_valid_input(text):
            """
            Проверяет, содержит ли текст только буквы, цифры и/или символы.
            Текст не должен содержать только символы без букв или цифр и не должен включать эмодзи.
            """
            # Паттерн для проверки: должен содержать хотя бы одну букву или цифру

            pattern = re.compile(
                r'^(?=.*[A-Za-z0-9а-яА-ЯёЁ])[A-Za-z0-9а-яА-ЯёЁ №!\"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~]+$')

            return bool(pattern.match(text))

        if parameter_name in ('mileage', 'year'):
            return

        valid_input = await is_valid_input(inputted_value)
        ic()
        ic(valid_input)
        if not valid_input:
            incorrect_flag = '(text_symbols)'

            return incorrect_flag


    async def used_car_parameters_validator(self, parameter_name, inputted_value):
        if not parameter_name in ('mileage', 'year'):
            return
        incorrect_flag = None
        from config_data.config import max_integer_for_database

        only_digit_value = inputted_value.replace('-', '').replace('+', '').replace(' ', '').replace('.', '')
        ic(only_digit_value)
        one_nodigit_type_limit = not any(inputted_value.count(symbol) > 1 for symbol in ('+', '-'))
        one_symbol_limit = not all(symbol in inputted_value for symbol in ('+', '-'))
        point_limit = inputted_value.count('.') <= 6
        valid_number = not inputted_value.startswith(('-', '.', '+'))
        input_value_not_null = not any(value_part.startswith('0') for value_part in only_digit_value)
        plus_correct_position = inputted_value.endswith('+') if '+' in inputted_value else True
        if all((only_digit_value.isdigit(), one_nodigit_type_limit, one_symbol_limit, point_limit, valid_number,
                plus_correct_position, input_value_not_null)):
            inputted_value_for_deep_validate = inputted_value.replace('+', '').replace('.', '').split('-')

            if len(inputted_value_for_deep_validate) == 2:
                if all(value_part.strip().isdigit() for value_part in inputted_value_for_deep_validate):
                    if not int(inputted_value_for_deep_validate[0]) < int(inputted_value_for_deep_validate[1]):
                        incorrect_flag = '(symbols)'

            elif not inputted_value.replace('.', '').split('-')[0].endswith('+'):
                incorrect_flag = '(symbols)'

            if not incorrect_flag:
                match parameter_name:
                    case 'mileage':
                        if int(only_digit_value) > max_integer_for_database:
                            incorrect_flag = '(int_len)'

                    case 'year':
                        current_year = datetime.now().year
                        if len(inputted_value) > 9 + inputted_value.count('.'):
                            incorrect_flag = '(year_len)'
                        elif any(current_year < int(year_part) if year_part.isdigit() else False\
                                 for year_part in inputted_value_for_deep_validate)\
                                and not ic(all(len(year_part) == 4 for year_part in inputted_value_for_deep_validate)):
                            incorrect_flag = '(year_len)'

        else:
            incorrect_flag = '(symbols)'
        ic()
        ic(parameter_name, one_symbol_limit, one_nodigit_type_limit, one_symbol_limit, incorrect_flag,
           plus_correct_position, input_value_not_null)
        return incorrect_flag
    @staticmethod
    async def get_returning_method(request, state):
        Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        current_state = str(await state.get_state())
        match current_state:
            case 'AdminAdvertParametersStates:start_add_value_process':
                message_input_request_handler = AddNewValueAdvertParameter().callback_handler
            case 'AdminAdvertParametersStates:start_rewrite_exists_parameter' | 'AdminAdvertParametersStates:confirmation_rewrite_exists_parameter':
                message_input_request_handler = RewriteExistsAdvertParameterHandler().callback_handler
            case _:#
                await send_message_answer(request, Lexicon_module.ADVERT_PARAMETERS_LEXICON['memory_was_forgotten'])
                return await AdvertParametersChooseCarState().callback_handler(request, state)

        return message_input_request_handler

    async def seek_matched_new_state_param_names(self, request, state: FSMContext, last_advert_parameter, parameter_value):
        output_specific_parameters_module = importlib.import_module(
            'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters')

        # await state.update_data()

        exists_params = await output_specific_parameters_module\
            .OutputSpecificAdvertParameters().get_need_new_car_state_params(request, state, last_advert_parameter)
        # exists_param = await CarConfigs.custom_action(mode=last_advert_parameter, action='get_by_name',
        #                                               name=parameter_value)
        ic(exists_params)
        if exists_params:
            exists_names = [param.name for param in exists_params]
            if parameter_value in exists_names:
                return True
        # if current_params:
        #     current_names = [param.name for param in current_params]
        #     if parameter_value in current_names:
        #         return True

