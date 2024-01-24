import importlib

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.memory_storage_incorrect_controller import \
    incorrect
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_tariff_data import process_tariff_cost, \
    process_write_tariff_cost
from handlers.utils.delete_message import delete_message


class DigitFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool | dict:

        config_module = importlib.import_module('config_data.config')

        is_correct = message.text.isdigit() and len(str(message.text)) < config_module.max_price_len and message.text[0] != '0'



        current_state = str(await state.get_state())
        memory_storage = await state.get_data()
        last_admin_answer = memory_storage.get('last_admin_answer')

        match current_state:
            case 'TariffAdminBranchStates:write_tariff_feedbacks_residual':
                callable_object = process_write_tariff_cost
            case _:
                callable_object = None

        if last_admin_answer:
            await delete_message(message, last_admin_answer)
        ic(is_correct)
        ic()
        if not is_correct:
            await incorrect(state, message.message_id)
            await callable_object(message, state, incorrect=True)

        else:
            await delete_message(message, message.message_id)
            return {'number': message.text}