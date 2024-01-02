from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config_data.config import car_configurations_in_keyboard_page
from database.data_requests.car_configurations_requests import CarConfigs
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import AdvertParametersChooseState
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler, InlinePaginationInit


class AdvertParametersChooseCarState(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        if not await state.get_state() == AdminAdvertParametersStates.review_process:
            await state.set_state(AdminAdvertParametersStates.review_process)

        self.output_methods = [
            InlinePaginationInit(
                lexicon_class=AdvertParametersChooseState,
                models_range=await CarConfigs.get_all_states(),
                page_size=car_configurations_in_keyboard_page
            )
        ]
