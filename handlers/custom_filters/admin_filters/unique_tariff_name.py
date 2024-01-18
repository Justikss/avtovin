import importlib

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.memory_storage_incorrect_controller import \
    incorrect
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_tariff_data import \
    process_write_tariff_time_duration
from handlers.utils.delete_message import delete_message


class UniqueTariffNameFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        config_module = importlib.import_module('config_data.config')
        tariff_requester_module = importlib.import_module('database.data_requests.tariff_requests')

        name = message.text.strip()
        match_name_tariff = await tariff_requester_module.TarifRequester.get_tariff_by_name(name)
        ic(match_name_tariff)
        if not match_name_tariff:
            match_name_tariff = ic(len(name.replace('<', '&lt;').replace('>', '&gt;'))) > ic(config_module.max_contact_info_len)
            ic(match_name_tariff)
        memory_storage = await state.get_data()

        last_admin_answer = memory_storage.get('last_admin_answer')
        if last_admin_answer:
            await delete_message(message, last_admin_answer)

        if not match_name_tariff:
            await delete_message(message, message.message_id)
            return {'message_text': message.text.replace('<', '&lt;').replace('>', '&gt;')}
        else:
            await incorrect(state, message.message_id)
            return await process_write_tariff_time_duration(message, state, incorrect=True)
