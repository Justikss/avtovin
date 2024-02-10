import importlib
import logging
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_params_class_lexicon
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from utils.oop_handlers_engineering.update_handlers.base_objects.base_handler import InlinePaginationInit


class AdvertParametersChooseCarState(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic()
        ic(type(request))
        await self.incorrect_manager.try_delete_incorrect_message(request, state)
        await self.set_state(state, AdminAdvertParametersStates.review_process)
        await state.update_data(next_params_output=None)
        await state.update_data(selected_parameters=None)
        await state.update_data(add_new_branch_status=None)
        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=advert_params_class_lexicon['car_parameters_start'],
                dynamic_buttons=2,
                delete_mode=True
            )
        ]
