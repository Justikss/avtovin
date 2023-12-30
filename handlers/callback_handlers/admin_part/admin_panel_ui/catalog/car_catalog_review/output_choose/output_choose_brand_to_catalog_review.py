import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config_data.config import admin_brand_pagination_pagesize
from database.data_requests.statistic_requests.adverts_to_admin_view_status import \
    advert_to_admin_view_related_requester
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler import output_choose
from states.admin_part_states.catalog_states.catalog_review_states import AdminCarCatalogReviewStates
from utils.lexicon_utils.Lexicon import CATALOG_LEXICON
from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import AdminReviewCatalogChooseCarBrand


async def try_set_correct_state(callback: CallbackQuery, state: FSMContext):
    if 'car_catalog_review__' in callback.data:
        if callback.data.endswith('__new'):
            current_state = AdminCarCatalogReviewStates.check_new_adverts
        elif callback.data.endswith('__viewed'):
            current_state = AdminCarCatalogReviewStates.check_viewed_adverts
        else:
            current_state = None

        if current_state:
            await state.set_state(current_state)

        correct_state = str(await state.get_state())
        view_status = 'viewed' in correct_state
        ic(view_status)

    else:
        view_status = None

    if view_status is None:
        memory_storage = await state.get_data()
        ic(memory_storage)
        view_status = memory_storage.get('advert_viewed_status')
    else:
        await state.update_data(advert_viewed_status=view_status)
    return view_status

async def choose_review_catalog_brand_admin_handler(callback: CallbackQuery, state: FSMContext):
    viewed_status = await try_set_correct_state(callback, state)
    ic(viewed_status)
    brand_models = await advert_to_admin_view_related_requester.retrieve_by_view_status(status=viewed_status, get_brands=True)
    ic(brand_models)
    await output_choose(callback, state, lexicon_class=AdminReviewCatalogChooseCarBrand,
                        models_range=brand_models, page_size=admin_brand_pagination_pagesize)

    await callback.answer()
