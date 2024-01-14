import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.mailing_requests import get_mailings_by_viewed_status
from handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_pagination import AdminPaginationOutput
from states.admin_part_states.mailing.mailing_review_states import MailingReviewStates



async def output_mailings(callback: CallbackQuery, state: FSMContext):
    mailing_ids = None
    if callback.data[-1].isdigit():
        viewed_status = int(callback.data.split(':')[-1])

        match viewed_status:
            case 1:
                state_object = MailingReviewStates.review_viewed_mailings
            case 0:
                state_object = MailingReviewStates.review_awaited_mailings
        await state.set_state(state_object)

        mailing_ids = await get_mailings_by_viewed_status(viewed_status, get_ids=True)

    if mailing_ids:

        await AdminPaginationOutput.set_pagination_data(callback, state, mailing_ids)
        ic()

    else:
        Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        await callback.answer(Lexicon_module.ADVERT_LEXICON['this_mailing_type_do_not_exists'])