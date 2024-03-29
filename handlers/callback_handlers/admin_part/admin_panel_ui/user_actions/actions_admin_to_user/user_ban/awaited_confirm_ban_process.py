import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest


from handlers.callback_handlers.admin_part.admin_panel_ui.utils.backward_from_user_output import \
    backward_from_user_profile_review
from handlers.utils.message_answer_without_callback import send_message_answer
from states.admin_part_states.users_review_states import SellerReviewStates, BuyerReviewStates

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def delete_mode_controller(state: FSMContext):
    memory_storage = await state.get_data()
    delete_mode = memory_storage.get('incorrect_flag')
    return delete_mode


async def set_confirmation_state(state: FSMContext, user_entity):
    ic(user_entity)
    match user_entity:
        case 'dealership' | 'seller':
            new_state = SellerReviewStates.confirmation_block_user

        case 'buyer':
            new_state = BuyerReviewStates.confirmation_block_user
        case _:
            return False

    await state.set_state(new_state)
    return True
async def ban_user_final_decision(message: Message, state: FSMContext, reason: str):
    admin_lexicon_module = importlib.import_module('utils.lexicon_utils.admin_lexicon.admin_lexicon')

    message_editor_module = importlib.import_module('handlers.message_editor')
    memory_storage = await state.get_data()
    user_entity_code = memory_storage.get('user_entity')
    lexicon_class = admin_lexicon_module.BanUser.InputReason(user_entity=user_entity_code,
                                        name=memory_storage.get('user_name'))
    if lexicon_class:
        if await set_confirmation_state(state, user_entity_code):

            if lexicon_class.user_entity:
                ic(lexicon_class.user_entity, reason)
                lexicon_part = Lexicon_module.ADMIN_LEXICON['final_decision_ban_user']
                lexicon_part['message_text'] = lexicon_part['message_text'].format(
                    user_entity=lexicon_class.user_entity,
                    reason=reason
                )

                delete_mode = await delete_mode_controller(state)

                return await message_editor_module.travel_editor.edit_message(request=message, lexicon_key='',
                                                                       lexicon_part=lexicon_part, delete_mode=delete_mode)

    await send_message_answer(message, Lexicon_module.ADMIN_LEXICON['action_non_actuality'], 1)

    await backward_from_user_profile_review(message, state)

