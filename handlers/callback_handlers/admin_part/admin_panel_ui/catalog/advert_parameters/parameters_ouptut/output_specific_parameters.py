from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config_data.config import car_configurations_in_keyboard_page
from database.data_requests.car_configurations_requests import CarConfigs
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import \
    AdvertSecondHandParametersChooseSpecificValue
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from utils.oop_handlers_engineering.update_handlers.base_objects.base_handler import InlinePaginationInit


class OutputSpecificAdvertParameters(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic(request.data)
        ic()
        if isinstance(request, CallbackQuery) and '_choice_advert_parameters_type_' in request.data:
            parameter_name = request.data.split('_')[-1]
            ic(parameter_name)
            await state.update_data(admin_chosen_advert_parameter=parameter_name)
        else:
            memory_storage = await state.get_data()
            parameter_name = memory_storage.get('admin_chosen_advert_parameter')

        ic(parameter_name)
        self.output_methods = [
            InlinePaginationInit(
                lexicon_class=AdvertSecondHandParametersChooseSpecificValue(parameter_name),
                models_range=await CarConfigs.get_or_insert(mode=parameter_name, action='get_*'),
                page_size=car_configurations_in_keyboard_page
            )]

        await self.set_state(state, AdminAdvertParametersStates.review_process)


