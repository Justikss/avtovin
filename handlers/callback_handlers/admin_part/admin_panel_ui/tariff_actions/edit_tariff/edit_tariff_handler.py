import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.tables.tariff import Tariff

from handlers.utils.message_answer_without_callback import send_message_answer
from states.admin_part_states.tariffs_branch_states import TariffEditState
from utils.get_currency_sum_usd import get_valutes


Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
admin_lexicon_module = importlib.import_module('utils.lexicon_utils.admin_lexicon.admin_lexicon')

async def tariff_edit_lexicon_part_constructor(tariff_model: Tariff, state: FSMContext):
    memory_storage = await state.get_data()
    nice_buttons = {}

    raw_lexicon_part = Lexicon_module.ADMIN_LEXICON['start_tariff_edit_action']

    tariff_edited_data = {
    'tariff_name': memory_storage.get('tariff_name'),
    'tariff_duration_time': memory_storage.get('tariff_duration_time'),
    'tariff_feedbacks_residual': memory_storage.get('tariff_feedbacks_residual'),
    'tariff_cost': memory_storage.get('tariff_cost')}
    ic(tariff_edited_data)
    await state.update_data(edited_tariff_data=tariff_edited_data)

    tariff_data = (tariff_model.name,
                   tariff_model.duration_time, tariff_model.feedback_amount, tariff_model.price)

    for callback_data, value in zip(raw_lexicon_part['buttons'], tariff_data):
        if not isinstance(value, str):
            value = str(value)

        if 'edit' in callback_data:
            edited_data = tariff_edited_data.get(callback_data.replace('edit_', ''))

            value = edited_data if edited_data else value

        if callback_data.endswith('time'):
            value = f'''{value} {admin_lexicon_module.captions['days']}'''
        elif callback_data.endswith('residual'):
            value = f'''{value} {admin_lexicon_module.captions['feedbacks']}'''
        elif callback_data.endswith('cost'):
            value = await get_valutes(None, int(value), get_string=True)
        nice_buttons[callback_data] = value

    for callback_data, caption in raw_lexicon_part['buttons'][-1].items():
        nice_buttons[callback_data] = caption

    lexicon_part = raw_lexicon_part
    lexicon_part['buttons'] = nice_buttons
    return lexicon_part

async def edit_tariff_by_admin_handler(request: CallbackQuery | Message, state: FSMContext):
    tariffs_requester_module = importlib.import_module('database.data_requests.tariff_requests')
    message_editor_module = importlib.import_module('handlers.message_editor')
    await state.update_data(edit_tariff_mode=True)
    memory_storage = await state.get_data()
    tariff_id = memory_storage.get('current_tariff_view')
    delete_mode = memory_storage.get('admin_incorrect_flag') is True
    tariff_model = await tariffs_requester_module.TarifRequester.get_by_id(tariff_id)
    if tariff_model:
        lexicon_part = await tariff_edit_lexicon_part_constructor(tariff_model, state)
        await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='',
                                                               lexicon_part=lexicon_part, delete_mode=delete_mode)
        await state.set_state(TariffEditState.waiting_for_field_choice)
    else:
        from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.output_tariff_list import \
            output_tariffs_for_admin
        await send_message_answer(request, Lexicon_module.ADMIN_LEXICON['tariff_was_inactive'], 1)
        await output_tariffs_for_admin(request, state)


async def field_choice_handler(callback: CallbackQuery, state: FSMContext):
    input_tariff_data_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_tariff_data')

    await state.set_state(TariffEditState.waiting_for_new_value)
    await state.update_data(edit_tariff_data=True)
    match callback.data:
        case 'edit_tariff_name':
            await input_tariff_data_module.process_write_tariff_time_duration(callback, state)
        case 'edit_tariff_duration_time':
            await input_tariff_data_module.process_write_tariff_feedbacks_residual(callback, state)
        case 'edit_tariff_feedbacks_residual':
            await input_tariff_data_module.process_write_tariff_cost(callback, state)
        case 'edit_tariff_cost':
            await input_tariff_data_module.process_tariff_cost(callback, state)


