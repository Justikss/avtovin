import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__choose_state import \
    AdvertParametersChooseCarState
from handlers.utils.message_answer_without_callback import send_message_answer
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates



async def seek_current_new_type_state(request: CallbackQuery | Message, state: FSMContext, delete_action: bool = False):
    memory_storage = await state.get_data()
    ic()
    delete_action = memory_storage.get('delete_params_flag')
    ic(delete_action)
    last_state = memory_storage.get('last_params_state')
    ic(last_state)
    ic()
    match last_state:
        case 'AdminAdvertParametersStates.NewStateStates:chosen_state':
            current_state = AdminAdvertParametersStates.NewStateStates.chosen_state
            previous_state = None
            # next_state = AdminAdvertParametersStates.NewStateStates.chosen_engine
        case 'AdminAdvertParametersStates.NewStateStates:chosen_engine':
            current_state = AdminAdvertParametersStates.NewStateStates.chosen_engine
            previous_state = AdminAdvertParametersStates.NewStateStates.chosen_state

#             next_state = AdminAdvertParametersStates.NewStateStates.chosen_brand
        case 'AdminAdvertParametersStates.NewStateStates:chosen_brand':
            current_state = AdminAdvertParametersStates.NewStateStates.chosen_brand
            previous_state = AdminAdvertParametersStates.NewStateStates.chosen_engine

#             next_state = AdminAdvertParametersStates.NewStateStates.chosen_model
        case 'AdminAdvertParametersStates.NewStateStates:chosen_model':
            current_state = AdminAdvertParametersStates.NewStateStates.chosen_model
            previous_state = AdminAdvertParametersStates.NewStateStates.chosen_brand

#             next_state = AdminAdvertParametersStates.NewStateStates.chosen_complectation
        case 'AdminAdvertParametersStates.NewStateStates:chosen_complectation':
            current_state = AdminAdvertParametersStates.NewStateStates.chosen_complectation
            previous_state = AdminAdvertParametersStates.NewStateStates.chosen_model

#             next_state = AdminAdvertParametersStates.NewStateStates.parameters_branch_review
        case 'AdminAdvertParametersStates.NewStateStates:chosen_color' | 'AdminAdvertParametersStates.NewStateStates:parameters_branch_review':
            current_state = AdminAdvertParametersStates.NewStateStates.parameters_branch_review
            previous_state = AdminAdvertParametersStates.NewStateStates.chosen_complectation

#             next_state = AdminAdvertParametersStates.NewStateStates.parameters_branch_review
        case _:#
            Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

            ic()
            await send_message_answer(request, Lexicon_module.ADVERT_PARAMETERS_LEXICON['memory_was_forgotten'])
            return await AdvertParametersChooseCarState().callback_handler(request, state)
    # match action:
    #     case 'delete':
    #         pass
    #     case 'edit':

    if delete_action and previous_state:
        current_state = previous_state
        await state.update_data(delete_params_flag=False)
    ic(current_state)
    await state.set_state(current_state)
