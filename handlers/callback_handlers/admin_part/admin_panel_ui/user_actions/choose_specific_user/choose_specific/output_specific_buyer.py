import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.tables.user import User
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_category.choose_users_category import \
    choose_user_category_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.utils.align_banned_data import \
    handle_banned_person_card
from states.admin_part_states.users_review_states import BuyerReviewStates
from utils.get_user_name import get_user_name
from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import pagination_interface


async def output_buyer_profile(request: CallbackQuery | Message, state: FSMContext, user_model=None, pagination: any=False):
    person_requester_module = importlib.import_module('database.data_requests.person_requests')
    message_editor_module = importlib.import_module('handlers.message_editor')
    Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    user_id = None
    memory_storage = await state.get_data()
    dynamic_buttons = 3
    await state.set_state(BuyerReviewStates.review_state)

    if not user_model:
        if isinstance(request, CallbackQuery):
            if request.data[-1].isdigit():
                user_id = request.data.split(':')[-1]
            else:
                user_id = memory_storage.get('current_user_id')
        user_model = user_id
    elif isinstance(user_model, list) and len(user_model) > 1:
        admin_pagination_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_pagination')
        await admin_pagination_module\
            .AdminPaginationOutput.set_pagination_data(request, state, [user.telegram_id for user in user_model])
        return
    elif isinstance(user_model, list):
        user_model = user_model[0]
    if user_model:
        ic(user_model)
        if not isinstance(user_model, User):
            ic(user_id)
            user_model = await person_requester_module.PersonRequester.get_user_for_id(user_id if user_id else user_model,
                                                                                       user=True)
            user_model = user_model[0]
            ic(user_model)
            ic()
        ic()
        # ic(user_id)
        await state.update_data(current_user_id=user_model.telegram_id)
        user_fullname, user_status = await get_user_name(user_model)
        lexicon_part = Lexicon_module.ADMIN_LEXICON['review_buyer_card']
        lexicon_part['message_text'] = lexicon_part['message_text'].format(full_name=user_fullname,
                                                                           phone_number=user_model.phone_number)
        if pagination:
            lexicon_part['buttons'] = {**pagination_interface, **lexicon_part['buttons']}
            lexicon_part['buttons']['width'] = (3, 1, 1, 1)
            lexicon_part['buttons']['page_counter'] = lexicon_part['buttons']['page_counter'].format(
                start=pagination.current_page,
                end=pagination.total_pages
            )
        ic(lexicon_part['buttons'])

        incorrect_flag = memory_storage.get('admin_incorrect_flag')
        if incorrect_flag:
            await state.update_data(incorrect_flag=False)

        if memory_storage.get('users_block_state') == 'true':
            lexicon_part = await handle_banned_person_card(lexicon_part, user_model)

        await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='',
                                                               lexicon_part=lexicon_part,
                                                               dynamic_buttons=dynamic_buttons,
                                                               delete_mode=not pagination or incorrect_flag)
    else:
        if isinstance(request, CallbackQuery):
            await request.answer(Lexicon_module.ADMIN_LEXICON['user_non_active'])
        await choose_user_category_by_admin_handler(request, state)