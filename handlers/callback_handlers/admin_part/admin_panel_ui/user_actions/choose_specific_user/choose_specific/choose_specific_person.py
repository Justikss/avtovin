import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config_data.config import user_pagesize_by_admin
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_category.choose_users_category import \
    choose_user_category_by_admin_handler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler import output_choose
from states.admin_part_states.users_review_states import SellerReviewStates, BuyerReviewStates
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON
from utils.lexicon_utils.admin_lexicon.admin_lexicon import SellerList, UserList
from handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_does_not_exists_handler import send_message_answer

async def construct_user_list_pagination_data(callback: CallbackQuery, state: FSMContext):
    person_requester_module = importlib.import_module('database.data_requests.person_requests')
    memory_storage = await state.get_data()

    if not isinstance(callback, CallbackQuery):
        user_mode = memory_storage.get('admin_review_user_mode')
    else:
        user_mode = callback.data.split('_')[0]
    ic()
    ic(user_mode)
    if user_mode not in ('buyer', 'seller'):
        ic()
        user_mode = memory_storage.get('admin_review_user_mode')

    ic(user_mode)
    if user_mode:
        if any(seller_entity in user_mode for seller_entity in ['legal', 'natural']):
            lexicon_class = SellerList(user_mode)
            ic(user_mode)
            users = await person_requester_module.PersonRequester.retrieve_all_data(seller=True, entity=user_mode)
            current_state = SellerReviewStates.review_state
        elif 'buyer' in user_mode:
            lexicon_class = UserList(user_mode)
            users = await person_requester_module.PersonRequester.retrieve_all_data(user=True)
            current_state = BuyerReviewStates.review_state
        else:
            current_state = None

        if current_state:
            await state.set_state(current_state)
        return lexicon_class, users


async def choose_specific_person_by_admin_handler(callback: CallbackQuery | Message, state: FSMContext, delete_redis_pagination_key=True, first_call=True):

    if first_call:
        await state.update_data(admin_review_user_mode=callback.data.split('_')[0])

    if delete_redis_pagination_key:
        redis_module = importlib.import_module('utils.redis_for_language')
        await redis_module.redis_data.delete_key(key=f'{callback.from_user.id}:inline_buttons_pagination_data')

    lexicon_class, users = await construct_user_list_pagination_data(callback, state)
    ic(lexicon_class, users)
    ic(users)
    if not users:
        alert_text = ADMIN_LEXICON['users_category_non_exists']
        current_state = str(await state.get_state())
        if isinstance(callback, CallbackQuery):
            await callback.answer(alert_text)
        else:
            await send_message_answer(callback, alert_text, 1)
        if current_state.startswith('BuyerReviewStates'):
            await choose_user_category_by_admin_handler(callback, state)
        return

    await output_choose(callback, state, lexicon_class, users, user_pagesize_by_admin)
