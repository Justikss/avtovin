import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from states.admin_part_states.catalog_states.catalog_review_states import AdminCarCatalogSearchByIdStates



admin_pagination_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_pagination')

async def inputted_advert_id_for_search_admin_handler(callback: CallbackQuery, state: FSMContext, advert_model):
    if await state.get_state() != AdminCarCatalogSearchByIdStates.review_searched_advert:
        await state.set_state(AdminCarCatalogSearchByIdStates.review_searched_advert)

    await admin_pagination_module.AdminPaginationOutput.set_pagination_data(callback, state, [advert_model.id])

    if isinstance(callback, CallbackQuery):
        await callback.answer()
