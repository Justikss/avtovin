from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config_data.config import car_configurations_in_keyboard_page
from database.data_requests.car_configurations_requests import CarConfigs
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import \
    AdvertSecondHandParametersChooseSpecificValue, advert_parameters_captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from utils.oop_handlers_engineering.update_handlers.base_objects.base_handler import InlinePaginationInit


class OutputSpecificAdvertParameters(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic(request.data)
        ic()
        message_text_header = ''

        if isinstance(request, CallbackQuery) and \
                ('_choice_advert_parameters_type_' or 'new_state_parameters:' in request.data):#'new_state_parameters:1_name'

            new_car_parameters_state = request.data.startswith('new')
            if new_car_parameters_state:
                memory_storage = await state.get_data()
                selected_parameters = memory_storage.get('selected_parameters')

                if not selected_parameters:
                    state_object = await CarConfigs.get_by_id('state', 1)
                    selected_parameters = f'''{advert_parameters_captions['state']}: {state_object.name}'''

                parameter_name = memory_storage.get('current_new_car_parameter')
                message_text_header = ADVERT_PARAMETERS_LEXICON['selected_new_car_params_pattern'].format(
                    params_data=selected_parameters)
            else:
                parameter_name = request.data.split('_')[-1]
                await state.update_data(admin_chosen_advert_parameter=parameter_name)
        else:
            memory_storage = await state.get_data()
            message_text_header = memory_storage.get('message_text_header')
            parameter_name = memory_storage.get('admin_chosen_advert_parameter')

        ic(parameter_name)
        self.output_methods = [
            InlinePaginationInit(
                lexicon_class=AdvertSecondHandParametersChooseSpecificValue(parameter_name, message_text_header),
                models_range=await CarConfigs.custom_action(mode=parameter_name, action='get_*'),
                page_size=car_configurations_in_keyboard_page
            )]

        await self.set_state(state, AdminAdvertParametersStates.review_process)


