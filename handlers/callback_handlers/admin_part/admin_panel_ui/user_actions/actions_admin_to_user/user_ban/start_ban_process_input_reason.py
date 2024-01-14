import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.callback_handlers.admin_part.admin_panel_ui.utils.backward_from_user_output import \
    backward_from_user_profile_review
from handlers.utils.message_answer_without_callback import send_message_answer
from utils.get_user_name import get_user_name

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def get_user_entity(callback: CallbackQuery, state: FSMContext):
    person_requester_module = importlib.import_module('database.data_requests.person_requests')

    current_state = str(await state.get_state())
    memory_storage = await state.get_data()

    user = True if current_state.startswith('BuyerReviewStates') else False
    seller = True if current_state.startswith('SellerReviewStates') else False

    if seller:
        user_id = memory_storage.get('current_seller_id')
    elif user:
        user_id = memory_storage.get('current_user_id')
    else:
        user_id = None

    ic(seller, user, user_id)
    if user_id:
        await state.update_data(user_id=user_id)
        user_model = await person_requester_module.PersonRequester.get_user_for_id(user_id, user=user, seller=seller)
        ic(user_model)
        if user_model:
            user_name, user_entity = await get_user_name(user_model)
            return user_name, user_entity

    return False

async def input_ban_reason_handler(request: CallbackQuery | Message, state: FSMContext, incorrect=False):
    message_editor_module = importlib.import_module('handlers.message_editor')

    user_data = await get_user_entity(request, state)
    if user_data:
        admin_lexicon_module = importlib.import_module('utils.lexicon_utils.admin_lexicon.admin_lexicon')

        user_name, user_entity = user_data
        await state.update_data(user_entity=user_entity)
        await state.update_data(user_name=user_name)
        lexicon_class = admin_lexicon_module.BanUser.InputReason(user_entity, user_name)
        lexicon_part = lexicon_class.lexicon_part
        if incorrect:
            lexicon_part['message_text'] = Lexicon_module.ADMIN_LEXICON['incorrect_input_block_reason'] + str(incorrect)
            reply_mode = request.message_id
        else:
            reply_mode = None
        await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='',
                                                       lexicon_part=lexicon_part, reply_message=reply_mode, delete_mode=True)
    else:
        alert_text = Lexicon_module.ADMIN_LEXICON['action_non_actuality']
        if isinstance(request, Message):
            await send_message_answer(request, alert_text, 1)
        else:
            await request.answer(alert_text)
        await backward_from_user_profile_review(request, state)
