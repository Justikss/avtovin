import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_parameters_captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters\
    .advert_parameters__second_hand_state_handlers.choose_parameter_type import TravelMessageEditorInit


Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


class AddNewValueAdvertParameter(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        incorrect_flag = await self.incorrect_manager.get_incorrect_flag(state)
        message_id = request.message_id if isinstance(request, Message) else None
        await self.try_set_add_new_state_params_state(state)
        self.output_methods = [
            TravelMessageEditorInit(
                lexicon_part=await self.lexicon_part_formatting(request, state, **kwargs),
                delete_mode=incorrect_flag or str(await state.get_state()) ==\
                            'AdminAdvertParametersStates.NewStateStates:parameters_branch_review' \
                            or kwargs.get('delete_mode'),
                reply_message=message_id if incorrect_flag else None
            )
        ]

        await self.set_state(state, AdminAdvertParametersStates.start_add_value_process)

    async def lexicon_part_formatting(self, request, state, **kwargs):
        memory_storage = await state.get_data()
        lexicon_part = await self.incorrect_manager.get_lexicon_part_in_view_of_incorrect(
                    lexicon_object=Lexicon_module.ADVERT_PARAMETERS_LEXICON,
                    lexicon_key='start_add_new_advert_parameter_value',
                    incorrect=kwargs.get('incorrect'))
        lexicon_part['message_text'] = lexicon_part['message_text'].format(
            parameter_name=advert_parameters_captions[
                memory_storage.get('admin_chosen_advert_parameter' if memory_storage.get('params_type_flag') != 'new'\
                                                                    else 'next_params_output')]
        )
        # if kwargs.get('add_new_branch_mode'):
        lexicon_part = await self.insert_into_lexicon_part_selected_params_header(state, lexicon_part)
        if memory_storage.get('params_type_flag') == 'new':
            lexicon_part['buttons'] = Lexicon_module.ADVERT_PARAMETERS_LEXICON['start_add_new_advert_parameter_value_new_state_buttons']
        return lexicon_part


    async def try_set_add_new_state_params_state(self, state: FSMContext):
        memory_storage = await state.get_data()

        ic()
        ic(memory_storage.get('params_type_flag'))
        ic(memory_storage.get('add_new_branch_status'))
        ic(memory_storage.get('can_set_add_new_branch_status'))

        if memory_storage.get('params_type_flag') == 'new':
            if not memory_storage.get('add_new_branch_status') and\
                    not memory_storage.get('can_set_add_new_branch_status'):
                await state.update_data(can_set_add_new_branch_status=True)


    async def insert_into_lexicon_part_selected_params_header(self, state: FSMContext, lexicon_part):

        memory_storage = await state.get_data()
        # memory_storage.get('can_set_add_new_branch_status') or memory_storage.get('add_new_branch_status') \
        # or
        if ic(memory_storage.get('params_type_flag')) == 'new':
            output_specific_parameters_module = importlib.import_module(
                'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters')

            message_text = await output_specific_parameters_module \
                .OutputSpecificAdvertParameters().construct_message_text_header_for_new_state_choose(state)
            lexicon_part['message_text'] = f'''{Lexicon_module.ADVERT_PARAMETERS_LEXICON['selected_new_car_params_pattern'].format(
                params_data=message_text
            )}{lexicon_part['message_text']}'''

        return lexicon_part
