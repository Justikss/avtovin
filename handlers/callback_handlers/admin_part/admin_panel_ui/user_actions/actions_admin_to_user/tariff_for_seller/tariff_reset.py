import importlib
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.admin_requests import AdminManager
from database.data_requests.person_requests import PersonRequester
from database.data_requests.tariff_to_seller_requests import TariffToSellerBinder
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.tariff_for_seller.checkout_tariff_by_admin import \
    construct_review_tariff_by_admin
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person import \
    choose_specific_person_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_seller import \
    output_specific_user_profile_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_does_not_exists_handler import \
    admin_does_not_exists_handler, admin_exists_checker
from utils.custom_exceptions.database_exceptions import AdminDoesNotExistsError
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action


async def construct_confirm_reset_request_lexicon_part(callback: CallbackQuery, state: FSMContext):
    header = await construct_review_tariff_by_admin(callback, state, get_header=True)
    lexicon_part = ADMIN_LEXICON['reset_tariff_confirm_request']
    lexicon_part['message_text'] = f'''{header}{lexicon_part['message_text']}'''
    return lexicon_part


async def tariff_reset_for_seller_from_admin_handler(callback: CallbackQuery, state: FSMContext):
    message_editor_module = importlib.import_module('handlers.message_editor')

    lexicon_part = await construct_confirm_reset_request_lexicon_part(callback, state)
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

async def confirm_action_reset_seller_tariff(callback: CallbackQuery, state: FSMContext):
    memory_storage = await state.get_data()
    seller_id = memory_storage.get('current_seller_id')

    reset_query = await TariffToSellerBinder.remove_bind(seller_id)


    if reset_query:
        await callback.answer(ADMIN_LEXICON['tariff_was_reset'])
        await output_specific_user_profile_handler(callback, state)
        await log_admin_action(admin_username=callback.from_user.username,
                               action='reset_tariff_action',
                               subject=f'seller:{seller_id}')
    else:
        await callback.answer(ADMIN_LEXICON['action_non_actuality'])
        await choose_specific_person_by_admin_handler(callback, state,
                                                      first_call=False)