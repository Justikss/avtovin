from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__choose_state import \
    AdvertParametersChooseCarState
from handlers.utils.message_answer_without_callback import send_message_answer
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from utils.lexicon_utils.Lexicon import ADVERT_PARAMETERS_LEXICON


async def seek_current_new_type_state(request: CallbackQuery | Message, state: FSMContext, action: str = None):
    memory_storage = await state.get_data()
    last_state = memory_storage.get('last_params_state')

    match last_state:
        case 'AdminAdvertParametersStates.NewStateStates:chosen_state':
            current_state = AdminAdvertParametersStates.NewStateStates.chosen_state
            # next_state = AdminAdvertParametersStates.NewStateStates.chosen_engine
        case 'AdminAdvertParametersStates.NewStateStates:chosen_engine':
            current_state = AdminAdvertParametersStates.NewStateStates.chosen_engine
#             next_state = AdminAdvertParametersStates.NewStateStates.chosen_brand
        case 'AdminAdvertParametersStates.NewStateStates:chosen_brand':
            current_state = AdminAdvertParametersStates.NewStateStates.chosen_brand
#             next_state = AdminAdvertParametersStates.NewStateStates.chosen_model
        case 'AdminAdvertParametersStates.NewStateStates:chosen_model':
            current_state = AdminAdvertParametersStates.NewStateStates.chosen_model
#             next_state = AdminAdvertParametersStates.NewStateStates.chosen_complectation
        case 'AdminAdvertParametersStates.NewStateStates:chosen_complectation':
            current_state = AdminAdvertParametersStates.NewStateStates.chosen_complectation
#             next_state = AdminAdvertParametersStates.NewStateStates.parameters_branch_review
        case 'AdminAdvertParametersStates.NewStateStates:chosen_color' | 'AdminAdvertParametersStates.NewStateStates:parameters_branch_review':
            current_state = AdminAdvertParametersStates.NewStateStates.parameters_branch_review
#             next_state = AdminAdvertParametersStates.NewStateStates.parameters_branch_review
        case _:#
            await send_message_answer(request, ADVERT_PARAMETERS_LEXICON['memory_was_forgotten'])
            return await AdvertParametersChooseCarState().callback_handler(request, state)
    # match action:
    #     case 'delete':
    #         pass
    #     case 'edit':

    await state.set_state(current_state)
