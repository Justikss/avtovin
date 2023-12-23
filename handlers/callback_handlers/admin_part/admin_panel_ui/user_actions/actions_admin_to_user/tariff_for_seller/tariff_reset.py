import importlib
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.tariff_for_seller.checkout_tariff_by_admin import \
    construct_review_tariff_by_admin
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_seller import \
    output_specific_seller_profile_handler
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
    tariff_to_seller_binder_module = importlib.import_module('database.data_requests.tariff_to_seller_requests')
    choose_specific_person_by_admin_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person')

    memory_storage = await state.get_data()
    seller_id = memory_storage.get('current_seller_id')

    reset_query = await tariff_to_seller_binder_module.TariffToSellerBinder.remove_bind(seller_id)


    if reset_query:
        await callback.answer(ADMIN_LEXICON['tariff_was_reset'])
        await output_specific_seller_profile_handler(callback, state)
        await log_admin_action(admin_username=callback.from_user.username,
                               action='reset_tariff_action',
                               subject=f'seller:{seller_id}')
    else:
        await callback.answer(ADMIN_LEXICON['action_non_actuality'])
        await choose_specific_person_by_admin_module.choose_specific_person_by_admin_handler(callback, state,
                                                      first_call=False)