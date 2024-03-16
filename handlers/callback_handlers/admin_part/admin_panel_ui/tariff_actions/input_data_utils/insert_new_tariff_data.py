import importlib
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import Message


from handlers.utils.message_answer_without_callback import send_message_answer
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action


async def insert_tariff_data(message: Message, state: FSMContext):
    Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    tariff_request_module = importlib.import_module('database.data_requests.tariff_requests')

    memory_storage = await state.get_data()
    cost = memory_storage.get('tariff_cost')
    feedbacks = memory_storage.get('tariff_feedbacks_residual')
    name = memory_storage.get('tariff_name')
    duration_time = memory_storage.get('tariff_duration_time')

    insert_data = {
        'name': name,
        'price': cost,
        'duration_time': duration_time,
        'feedback_amount': feedbacks
    }
    ic(insert_data)

    insert_query = await tariff_request_module.TarifRequester.set_tariff(insert_data)
    ic(insert_query)

    if insert_query:
        alert_text = Lexicon_module\
                .ADMIN_LEXICON['success_input_tariff_data'].format(tariff_name=insert_query.name)
        await log_admin_action(message.from_user.username, 'add_tariff', insert_query)
    else:
        logging.warning(f'Администратор {message.from_user.username} неудачно добавил тариф')

        alert_text = Lexicon_module\
                .ADMIN_LEXICON['unsuccessfully_add_tariff']

    await send_message_answer(message, alert_text, 1)
    from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.output_tariff_list import \
        output_tariffs_for_admin
    await output_tariffs_for_admin(message, state)
