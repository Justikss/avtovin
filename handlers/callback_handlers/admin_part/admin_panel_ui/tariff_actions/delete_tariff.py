import importlib
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.output_tariff_list import \
    output_tariffs_for_admin
from utils.custom_exceptions.database_exceptions import TariffHasWireError
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def delete_tariff_model_by_admin(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    lexicon_part = Lexicon_module\
        .ADMIN_LEXICON['tariff_delete_confirm_action']

    await message_editor.travel_editor.edit_message(
        request=callback, lexicon_key='', lexicon_part=lexicon_part
    )

async def confirm_delete_tariff_action(callback: CallbackQuery, state: FSMContext):
    tariff_requests_module = importlib.import_module('database.data_requests.tariff_requests')

    memory_storage = await state.get_data()
    tariff_id = memory_storage.get('current_tariff_view')

    # try:
    delete_query = await tariff_requests_module.TarifRequester.set_dying_tariff_status(tariff_id)
    #
    # except TariffHasWireError:
    #     return await callback.answer(Lexicon_module\
    #     .ADMIN_LEXICON['tariff_has_bindings'], show_alert=True)

    await state.update_data(current_tariff_view=None)
    if delete_query:
        alert_text = Lexicon_module\
            .ADMIN_LEXICON['tariff_was_successfully_removed']
        await log_admin_action(callback.from_user.username, 'delete_tariff', f'tariff:{tariff_id}')
    else:
        logging.warning(f'Администратор {callback.from_user.username} неудачно удалил тариф ID: {tariff_id}')

        alert_text = Lexicon_module\
            .ADMIN_LEXICON['tariff_was_inactive']

    await callback.answer(alert_text)
    await output_tariffs_for_admin(callback, state)
