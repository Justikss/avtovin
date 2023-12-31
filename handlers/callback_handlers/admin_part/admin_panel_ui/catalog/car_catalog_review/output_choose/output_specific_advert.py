import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.statistic_requests.adverts_to_admin_view_status import \
    advert_to_admin_view_related_requester
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.car_catalog_review.output_choose.output_choose_brand_to_catalog_review import \
    choose_review_catalog_brand_admin_handler
from handlers.utils.message_answer_without_callback import send_message_answer
from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import catalog_captions


async def output_review_adverts_catalog_admin_handler(callback: CallbackQuery, state: FSMContext):
    admin_pagination_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_pagination')
    memory_storage = await state.get_data()

    if callback.data[-1].isdigit():
        brand_id = int(callback.data.split(':')[-1])
        await state.update_data(selected_catalog_brand=brand_id)
    else:
        brand_id = memory_storage.get('selected_catalog_brand')

    advert_ids = await advert_to_admin_view_related_requester.retrieve_by_view_status(
        status=memory_storage.get('advert_viewed_status'),
        get_by_brand=brand_id
    )

    ic(advert_ids)
    if advert_ids:
        await admin_pagination_module.AdminPaginationOutput.set_pagination_data(callback, state, advert_ids)
        await callback.answer()
    else:
        await send_message_answer(callback, catalog_captions['inactive_advert_or_seller'])
        await choose_review_catalog_brand_admin_handler(callback, state)
