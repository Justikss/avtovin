import importlib

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.input_name_to_search.start_input_name_request import \
    input_person_name_to_search_request_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_buyer import \
    output_buyer_profile
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_seller import \
    output_specific_seller_profile_handler
from states.admin_part_states.users_review_states import SellerReviewStates, BuyerReviewStates


async def delete_deprivation_user_answers(message, state):
    memory_storage = await state.get_data()

    if memory_storage.get('admin_incorrect_flag'):
        message_id = memory_storage.get('last_admin_message')
        if message_id:
            try:
                await message.chat.delete_message(message_id)
            except TelegramBadRequest:
                pass
    try:
        await message.chat.delete_message(message_id=message.message_id)
    except TelegramBadRequest:
        pass

async def inputted_name_from_admin_handler(message: Message, state: FSMContext, user_name):
    person_requester_module = importlib.import_module('database.data_requests.person_requests')
    ic(user_name)
    current_state = str(await state.get_state())
    memory_storage = await state.get_data()

    seller_search = False
    callable_object = None
    buyer_search = False
    dealership_search = False
    ic(current_state)
    match current_state:
        case 'SellerReviewStates:legal_entity_search':
            dealership_search = True
            seller_search = True
            good_state_object = SellerReviewStates.review_state
            callable_object = output_specific_seller_profile_handler
        case 'SellerReviewStates:natural_entity_search':
            good_state_object = SellerReviewStates.review_state
            seller_search = True
            callable_object = output_specific_seller_profile_handler
        case 'BuyerReviewStates:buyer_entity_search':
            good_state_object = BuyerReviewStates.review_state
            buyer_search = True
            callable_object = output_buyer_profile

    result_user = await person_requester_module.PersonRequester.get_by_user_name(user_name, user=buyer_search,
                                                                            seller=seller_search,
                                                                            dealership=dealership_search,
                                                                                 banned_status=memory_storage.get('users_block_state'))
    ic(result_user)
    if result_user:
        await state.set_state(good_state_object)
        await delete_deprivation_user_answers(message, state)
        # user_id = str(result_user.telegram_id)

        await callable_object(message, state, result_user)

        # choose_specific_person_by_admin_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person')
        #
        # await choose_specific_person_by_admin_module.choose_specific_person_by_admin_handler(message, state,
        #                                               first_call=False)
    else:
        ic(await state.update_data(incorrect_message=message.message_id))
        await input_person_name_to_search_request_handler(message, state, incorrect='(non_exists)')