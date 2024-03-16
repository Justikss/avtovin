import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_parameters_captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_message_handler_init import BaseMessageHandler
import traceback
Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


class ConfirmationRewriteExistsAdvertParameterHandler(BaseMessageHandler):
    async def process_message(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic()
        if await self.check_on_exists_branch(request, state, request.text):
            self.output_methods = []
            return
        traceback.print_stack()

        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=await self.insert_data_into_message_text(request, state),
                delete_mode=await self.incorrect_manager.get_incorrect_flag(state)
            )
        ]
        ic(self.output_methods)
        ic()
        await state.set_state(AdminAdvertParametersStates.confirmation_rewrite_exists_parameter)
        # await super().process_message(request, state, **kwargs)

    async def check_on_exists_branch(self, request, state, complectation=None):
        new_car_state_parameters_module = importlib.import_module(
            'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.new_car_state_parameters_handler')

        current_parameter_name, current_parameter_value = await new_car_state_parameters_module\
            .NewCarStateParameters().get_last_selected_param(state)
        ic(current_parameter_name, complectation)
        if current_parameter_name == 'complectation':
            from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.add_new_branch_confirm.confirm_add_new_branch_handler import \
                ConfirmLoadNewParamsBranchHandler
            if await ConfirmLoadNewParamsBranchHandler().exists_branch(state, rewriting_complectation=complectation):
                await state.update_data(rewriting_complectation=None)
                await self.send_alert_answer(request, Lexicon_module.ADMIN_LEXICON['branch_is_exists'])
                from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_rewriting.start import \
                    RewriteExistsAdvertParameterHandler
                await RewriteExistsAdvertParameterHandler().callback_handler(request, state)
                return True


    async def insert_data_into_message_text(self, request, state):
        new_car_state_parameters_module = importlib.import_module(
            'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.new_car_state_parameters_handler')

        ic()

        memory_storage = await state.get_data()
        # current_parameter_name = memory_storage.get('admin_chosen_advert_parameter')
        # current_parameter_value = memory_storage.get('current_advert_parameter')['value']
        current_parameter_name, current_parameter_value = await new_car_state_parameters_module\
            .NewCarStateParameters().get_last_selected_param(state)

        new_parameter_value = request.text
        if memory_storage.get('current_new_parameter_value') != new_parameter_value:
            await state.update_data(current_new_parameter_value=new_parameter_value)

        lexicon_part = await self.insert_into_message_text(
            Lexicon_module.ADVERT_PARAMETERS_LEXICON['confirmation_rewrite_exists_parameter'],
            {'parameter_type': advert_parameters_captions[current_parameter_name],
             'parameter_old_value': current_parameter_value,
             'parameter_new_value': new_parameter_value}
        )
        ic(lexicon_part)
        return lexicon_part