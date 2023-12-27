import importlib
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.output_specific_tariff import \
    output_specific_tariff_for_admin_handler
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action


async def insert_tariff_data(callback: CallbackQuery, state: FSMContext):
    tariff_requests_module = importlib.import_module('database.data_requests.tariff_requests')

    memory_storage = await state.get_data()
    edited_tariff_data = memory_storage.get('edited_tariff_data')
    tariff_id = memory_storage.get('current_tariff_view')

    boot_data_keys = ('name', 'duration_time', 'feedback_amount', 'price')

    tariff_model = await tariff_requests_module.TarifRequester.get_by_id(tariff_id)

    good_boot_data = {}
    ic(boot_data_keys, edited_tariff_data)
    for string_name, value in zip(boot_data_keys, edited_tariff_data.values()):
        if not value:
            value = getattr(tariff_model, string_name)

        good_boot_data[string_name] = value
    ic(good_boot_data)
    await tariff_requests_module.TarifRequester.set_dying_tariff_status(tariff_id)

    insert_response = await tariff_requests_module.TarifRequester.set_tariff(good_boot_data)
    if insert_response:
        await log_admin_action(callback.from_user.username, 'edit_tariff', insert_response)
        await state.update_data(current_tariff_view=insert_response.id)
        await callback.answer(ADMIN_LEXICON['successfully_edit_action'])
        await output_specific_tariff_for_admin_handler(callback, state)
    else:
        logging.warning(f'Администратор {callback.from_user.username} неудачно отредактировал тариф {tariff_model.name}')

    await state.update_data(tariff_name=None)
    await state.update_data(tariff_duration_time=None)
    await state.update_data(tariff_feedbacks_residual=None)
    await state.update_data(tariff_cost=None)
    await state.update_data(edited_tariff_data=None)





