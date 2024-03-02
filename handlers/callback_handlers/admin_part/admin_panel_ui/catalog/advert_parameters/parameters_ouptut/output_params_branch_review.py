import importlib
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.new_car_photo_requests import PhotoRequester
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.handling_exists_value_advert_parameter.action_of_deletion.start_deletion import TravelMessageEditorInit

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

class ParamsBranchReviewHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # OutputSpecificAdvertParameters().check_state_on_add_new_branch_status(state)
        output_specific_parameters_module = importlib.import_module(
            'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters')
        traceback.print_stack()
        ic(await state.get_data())
        # traceback.print_stack()
        media_group = kwargs.get('media_photos')
        memory_storage = await self.get_memory_storage(state)
        ic()
        ic(memory_storage)
        selected_parameters = memory_storage.get('selected_parameters')
        second_hand_mode = kwargs.get('second_hand_mode')
        change_state_flag = await self.get_from_memory_storage(state, 'change_state_flag')
        ic(second_hand_mode, media_group, change_state_flag, memory_storage.get('add_new_branch_status'))
        if change_state_flag == 'from_used':
            second_hand_mode = 'update_state'
        # if not second_hand_mode:
        if not media_group:
            media_group = selected_parameters.get('photos')

        if media_group or (second_hand_mode and second_hand_mode != 'second_hand_review'):

            memory_storage = await state.get_data()
            ic(selected_parameters)

            if media_group:
                await self.update_photo_pack_in_load_system(state, media_group)
            # if not second_hand_mode:
            state_to_set = AdminAdvertParametersStates.NewStateStates.confirmation_new_params_branch_to_load
            # else:
            #     state_to_set = None
            lexicon_part = await self.message_text_modifier(state, second_hand_mode)
        else:
            state_to_set = AdminAdvertParametersStates.NewStateStates.parameters_branch_review
            lexicon_part = Lexicon_module.ADVERT_PARAMETERS_LEXICON['review_params_branch']

            ic(str(selected_parameters.get('state')) == '2', selected_parameters, str(selected_parameters.get('state')))



            if any(str(state_param) == '2' for state_param in (selected_parameters.get('state'),
                                                               memory_storage.get('new_state'))):

                media_group = None
            else:
                media_group = await PhotoRequester.try_get_photo(state, for_admin=True)

        if str(selected_parameters.get('state')) == '2' and not media_group:
            ic(lexicon_part)
            del lexicon_part['buttons']['update_params_branch_media_group']
            ic(lexicon_part.get('update_params_branch_media_group'))

        ic(state_to_set)
        if state_to_set:
            await self.set_state(state, state_to_set)
        message_text = await output_specific_parameters_module.OutputSpecificAdvertParameters().construct_message_text_header_for_new_state_choose(state)
        ic(media_group, message_text)
        lexicon_part['message_text'] = f'''{Lexicon_module.ADVERT_PARAMETERS_LEXICON['selected_new_car_params_pattern'].format(
            params_data=message_text
        )}{lexicon_part['message_text']}'''
        ic()
        ic(lexicon_part)
        menu_generate_method = TravelMessageEditorInit(lexicon_part=lexicon_part,
                                    media_group=media_group,
                                                       delete_mode=kwargs.get('delete_mode'))
        ic(menu_generate_method)
        ic(kwargs.get('make_output'))
        if kwargs.get('make_output'):
            self.output_methods = [
                menu_generate_method
            ]
            ic(len(self.output_methods))
            ic()
            # await self._output_panel(request, state)
            # return
        else:
            return menu_generate_method



    async def message_text_modifier(self, state: FSMContext, second_hand_mode):

        lexicon_part = Lexicon_module.ADVERT_PARAMETERS_LEXICON['load_new_params_branch_confirmation']
        current_state = str(await state.get_state())
        selected_parameters = await self.get_from_memory_storage(state, 'selected_parameters')
        memory_storage = await state.get_data()
        ic()
        ic(current_state)
        ic(second_hand_mode, memory_storage.get('change_state_flag'), memory_storage.get('update_photos'))
        if (not memory_storage.get('change_state_flag') and not second_hand_mode) and memory_storage.get('update_photos'):
            lexicon_part['message_text'] = Lexicon_module.ADVERT_PARAMETERS_LEXICON['update_photo_caption']
            ic(lexicon_part['buttons'].get('update_params_branch_state'), str(selected_parameters['state']))
            if str(selected_parameters['state']) == '1' and lexicon_part['buttons'].get('update_params_branch_state'):
                del lexicon_part['buttons']['update_params_branch_state']
        ic(second_hand_mode, selected_parameters.get('color'))
        ic(((not selected_parameters.get('color') or second_hand_mode == 'update_state')) and \
                second_hand_mode not in ('second_hand_review', 'add'), second_hand_mode not in ('second_hand_review', 'add'),
           (not selected_parameters.get('color') or second_hand_mode == 'update_state'))

        #if (not selected_parameters.get('color') or second_hand_mode == 'update_state') and \
        if second_hand_mode and \
            (second_hand_mode not in ('second_hand_review', 'add')):# and not memory_storage.get('add_new_branch_status'):
            lexicon_part['message_text'] = Lexicon_module.ADVERT_PARAMETERS_LEXICON['load_photo_to_change_state_confirmation']
        return lexicon_part
    async def update_photo_pack_in_load_system(self, state: FSMContext, media_group) -> None:
        memory_storage = await state.get_data()
        selected_parameters = memory_storage.get('selected_parameters')
        ic(selected_parameters)
        selected_parameters['photos'] = media_group
        await state.update_data(selected_parameters=selected_parameters)
