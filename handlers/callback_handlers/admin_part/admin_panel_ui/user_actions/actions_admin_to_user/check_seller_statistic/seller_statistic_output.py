import importlib
from copy import copy

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.tables.statistic_tables.period_seller_statistic import calculate_stats
from utils.get_user_name import get_user_name
from utils.lexicon_utils.Lexicon import STATISTIC_LEXICON, ADMIN_LEXICON
from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions


async def get_period_string(period):
    match period:
        case str() as period if period in ('day', 'week', 'month', 'year'):
            period = period
        case _:
            period = 'any'

    result = copy(captions[period])
    return result


async def handle_stats_callback(query: CallbackQuery, state: FSMContext):
    message_editor_module = importlib.import_module('handlers.message_editor')
    person_requester_module = importlib.import_module('database.data_requests.person_requests')

    memory_storage = await state.get_data()
    seller_id = memory_storage.get('current_seller_id')
    period = query.data.split(':')[-1]
    seller_model = await person_requester_module.PersonRequester.get_user_for_id(seller_id, seller=True)

    if seller_model:
        seller_model = seller_model[0] if isinstance(seller_model, list) else seller_model
        seller_name, entity = await get_user_name(seller_model)
        seller_date_of_registration = seller_model.data_registration

        adverts_count, feedbacks_count = await calculate_stats(seller_id, period)

        period_string = await get_period_string(period)
        lexicon_part = STATISTIC_LEXICON['seller_statistic_view']
        lexicon_part['message_text'] = lexicon_part['message_text'].format(seller_name=seller_name,
                                                                           date_of_registration=seller_date_of_registration,
                                                                           period=period_string, adverts_count=adverts_count,
                                                                           feedbacks_count=feedbacks_count)

        await query.answer(ADMIN_LEXICON['information_was_updated'])

        await message_editor_module.travel_editor.edit_message(request=query, lexicon_key='',
                                                               lexicon_part=lexicon_part)

    else:
        await query.answer(ADMIN_LEXICON['user_non_active'])
        choose_specific_person_by_admin_module = importlib.import_module(
            'handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person')
        await choose_specific_person_by_admin_module.choose_specific_person_by_admin_handler(query, state, first_call=False)


