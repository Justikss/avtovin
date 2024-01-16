import importlib
import logging
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import AdvertParametersChooseState
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from utils.oop_handlers_engineering.update_handlers.base_objects.base_handler import InlinePaginationInit


class AdvertParametersChooseCarState(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        config_module = importlib.import_module('config_data.config')
        car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')
        await self.set_state(state, AdminAdvertParametersStates.review_process)
        logging.debug("Стек вызовов: %s", traceback.format_stack())
        await state.update_data(next_params_output=None)
        await state.update_data(selected_parameters=None)
        self.output_methods = [
            InlinePaginationInit(
                lexicon_class=AdvertParametersChooseState,
                models_range=ic(await car_configs_module.CarConfigs.get_all_states()),
                page_size=config_module.car_configurations_in_keyboard_page
            )
        ]
