import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.tables.tariff import Tariff
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.output_tariff_list import \
    output_tariffs_for_admin
from states.admin_part_states.tariffs_branch_states import TariffEditState
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON


async def tariff_edit_lexicon_part_constructor(tariff_model: Tariff, state: FSMContext):
    memory_storage = await state.get_data()
    nice_buttons = {}

    raw_lexicon_part = ADMIN_LEXICON['start_tariff_edit_action']

    tariff_edited_data = {
    'tariff_name': memory_storage.get('tariff_name'),
    'tariff_duration_time': memory_storage.get('tariff_duration_time'),
    'tariff_feedbacks_residual': memory_storage.get('tariff_feedbacks_residual'),
    'tariff_cost': memory_storage.get('tariff_cost')}

    tariff_data = (tariff_model.name,
                   tariff_model.duration_time, tariff_model.feedback_amount, tariff_model.price)

    for callback_data, value in zip(raw_lexicon_part['buttons'], tariff_data):
        if not isinstance(value, str):
            value = str(value)
        if 'edit' in callback_data:
            edited_data = tariff_edited_data.get(value.replace('edit', ''))
            value = edited_data if edited_data else value
        nice_buttons[callback_data] = value

    ic(nice_buttons)
    ic()
    for callback_data, caption in raw_lexicon_part['buttons'][-1].items():
        nice_buttons[callback_data] = caption

    ic(nice_buttons)

    lexicon_part = raw_lexicon_part
    lexicon_part['buttons'] = nice_buttons
    return lexicon_part

async def edit_tariff_by_admin_handler(callback: CallbackQuery, state: FSMContext):
    tariffs_requester_module = importlib.import_module('database.data_requests.tariff_requests')
    message_editor_module = importlib.import_module('handlers.message_editor')

    memory_storage = await state.get_data()
    tariff_id = memory_storage.get('current_tariff_view')

    tariff_model = await tariffs_requester_module.TarifRequester.get_by_id(tariff_id)
    if tariff_model:
        lexicon_part = await tariff_edit_lexicon_part_constructor(tariff_model, state)
        await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='',
                                                               lexicon_part=lexicon_part)
        await state.set_state(TariffEditState.waiting_for_field_choice)
    else:
        await callback.answer(ADMIN_LEXICON['tariff_was_inactive'])
        await output_tariffs_for_admin(callback, state)


async def field_choice_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TariffEditState.waiting_for_new_value)

    match callback.data:
        case 'edit_tariff_name':

        case 'edit_tariff_duration_time':

        case 'edit_tariff_feedbacks_residual':

        case 'edit_tariff_cost':



