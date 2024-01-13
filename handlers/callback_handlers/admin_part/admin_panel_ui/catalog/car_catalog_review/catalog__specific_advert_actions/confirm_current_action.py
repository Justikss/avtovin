import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.car_advert_requests import AdvertRequester
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.car_catalog_review.catalog__specific_advert_actions.utils.delete_advert_by_admin import \
    delete_advert_admin_action
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.car_catalog_review.output_choose.output_specific_advert import \
    output_review_adverts_catalog_admin_handler
from handlers.utils.message_answer_without_callback import send_message_answer
from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import catalog_captions


async def confirm_specific_advert_action_admin_handler(callback: CallbackQuery, state: FSMContext):
    memory_storage = await state.get_data()
    action = memory_storage.get('advert_action_subject')
    current_advert_id = memory_storage.get('current_catalog_advert_id')
    current_seller_id = memory_storage.get('user_id')
    advert_model = await AdvertRequester.get_where_id(current_advert_id)
    ic(action, current_seller_id, current_advert_id, advert_model, memory_storage)
    if advert_model:
        if action == 'delete':
            await delete_advert_admin_action(callback, state, current_advert_id, current_seller_id)
            return await output_review_adverts_catalog_admin_handler(callback, state)
        elif action == 'block':
            confirm_block_user_action_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.user_ban.confirm_block_user_action')
            await confirm_block_user_action_module\
                    .confirm_user_block_action(callback, state)
    else:
        await send_message_answer(callback, catalog_captions['inactive_advert_or_seller'])


    await callback.answer()
