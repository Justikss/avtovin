from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class ChangeStateOnExistsBranchHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        if await self.feasibility_check(request, state):
            self.output_methods = [
                self.menu_manager.travel_editor(
                    lexicon_part=await self.construct_lexicon_part(state),
                    delete_mode=True
                )
            ]
        else:
            self.output_methods = []
    async def construct_lexicon_part(self, state: FSMContext):
        memory_storage = await state.get_data()

        selected_params = memory_storage.get('selected_parameters')
        ic(memory_storage.get('new_state'))
        selected_state = memory_storage.get('new_state') \
            if memory_storage.get('change_state_flag') \
            else selected_params['state']

        ic(selected_state)
        lexicon_part = self.lexicon_module.ADVERT_PARAMETERS_LEXICON['change_state']

        lexicon_part['buttons'] = {
            key: value for key, value in lexicon_part['buttons'].items()
                                      if not key.endswith(str(selected_state).lower())
        }

        return lexicon_part
    async def feasibility_check(self, request, state):
        from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_deletion.start_deletion import \
            ActionOfDeletionExistsAdvertParameter

        memory_storage = await state.get_data()
        selected_params = memory_storage.get('selected_parameters')
        if not memory_storage.get('add_new_branch_status'):
            exists_adverts = await ActionOfDeletionExistsAdvertParameter().check_on_exists_adverts_by_parameter(
                state, selected_params
            )
            ic(memory_storage.get('add_new_branch_status'))
            if exists_adverts:
                await self.send_alert_answer(request,
                                             self.lexicon_module.ADVERT_PARAMETERS_LEXICON['state_update_impossible'],
                                             message=True)

                from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_params_branch_review import \
                    ParamsBranchReviewHandler
                ic()
                print('ParamsBranchReviewHandler()cbh')
                await ParamsBranchReviewHandler().callback_handler(request, state, make_output=True)

                return False

        return True