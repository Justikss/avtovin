import importlib
import re

from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.edit_tariff.edit_data_controller import \
    edit_tariff_data_controller
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.incorrect_controller import \
    incorrect_controller, get_delete_mode
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.insert_new_tariff_data import \
    insert_tariff_data
from states.admin_part_states.tariffs_branch_states import TariffAdminBranchStates
from utils.get_currency_sum_usd import convertator


async def process_tariff_cost(request: types.Message | types.CallbackQuery, state: FSMContext, incorrect=False):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    if isinstance(request, types.CallbackQuery) and request.data[-1].isdigit():
        tariff_id = int(request.data.split(':')[-1])
        await state.update_data(specific_tariff_id=tariff_id)

    await state.set_state(TariffAdminBranchStates.write_tariff_cost)

    delete_mode = await get_delete_mode(state, incorrect)
    lexicon_part, reply_to_message = await incorrect_controller(request, state, incorrect, 'input_tariff_cost')
    ic()
    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                    delete_mode=delete_mode, reply_message=reply_to_message)


# Обработчик для записи стоимости тарифа
# @dp.message_handler(lambda message: message.text.isdigit(), state=TariffAdminBranchStates.write_tariff_cost)
async def process_write_tariff_cost(request: types.Message | types.CallbackQuery, state: FSMContext, incorrect=False,
                                    price=None, head_valute=None):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    if not incorrect:
        if price and head_valute:
            if head_valute == 'usd':
                price = await convertator(head_valute, price)
            await state.update_data(tariff_cost=int(price))
        await state.set_state(TariffAdminBranchStates.write_tariff_feedbacks_residual)

    if await edit_tariff_data_controller(request, state, incorrect):
        return
    delete_mode = await get_delete_mode(state, incorrect)
    ic(delete_mode)
    ic()
    lexicon_part, reply_to_message = await incorrect_controller(request, state, incorrect, 'input_tariff_feedbacks')
    ic(reply_to_message)
    await message_editor.travel_editor.edit_message(
        request=request, lexicon_key='', lexicon_part=lexicon_part,
        delete_mode=delete_mode if delete_mode else bool(reply_to_message) is True,
        reply_message=reply_to_message
    )


# Обработчик для записи количества откликов тарифа
# @dp.message_handler(lambda message: message.text.isdigit(), state=TariffAdminBranchStates.write_tariff_feedbacks_residual)
async def process_write_tariff_feedbacks_residual(request: types.Message | types.CallbackQuery, state: FSMContext, incorrect=False):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    if isinstance(request, types.Message) and not incorrect:
        await state.update_data(tariff_feedbacks_residual=int(request.text))

    if await edit_tariff_data_controller(request, state, incorrect):
        return

    lexicon_key = 'input_tariff_time_duration'

    await state.set_state(TariffAdminBranchStates.write_tariff_duration_time)

    delete_mode = await get_delete_mode(state, incorrect)
    lexicon_part, reply_to_message = await incorrect_controller(request, state, incorrect, lexicon_key)
    await message_editor.travel_editor.edit_message(
        request=request, lexicon_key='', lexicon_part=lexicon_part,
        delete_mode=delete_mode if delete_mode else bool(reply_to_message) is True,
        reply_message=reply_to_message
    )

async def process_write_tariff_time_duration(request: types.Message | types.CallbackQuery, state: FSMContext, incorrect=False):
    async def convert_to_days(time_string):
        # Проверка соответствия входной строки формату
        if not re.match(r'^\d+:\d+:\d+$', time_string):
            return False

        years, months, days = map(int, time_string.split(':'))

        # Предполагаем, что в году 365 дней, а в месяце 30 дней
        total_days = years * 365 + months * 30 + days
        return total_days

    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    memory_storage = await state.get_data()

    if not incorrect:
        if isinstance(request, types.Message):
            duration_time = await convert_to_days(request.text)
            ic(duration_time)
            await state.update_data(tariff_duration_time=duration_time)


    if await edit_tariff_data_controller(request, state, incorrect):
        return

    await state.set_state(TariffAdminBranchStates.write_tariff_name)
    lexicon_key = 'input_tariff_name'


    delete_mode = await get_delete_mode(state, incorrect)
    lexicon_part, reply_to_message = await incorrect_controller(request, state, incorrect, lexicon_key)
    await message_editor.travel_editor.edit_message(
        request=request, lexicon_key='', lexicon_part=lexicon_part,
        delete_mode=delete_mode if delete_mode else bool(reply_to_message) is True,
        reply_message=reply_to_message
    )

#Фильтр уникальности
async def process_tariff_name(request: types.Message | types.CallbackQuery, state: FSMContext):
    # Здесь мы просто сохраняем ввод названия тарифа и переходим к следующему состоянию
    if isinstance(request, types.Message):
        await state.update_data(tariff_name=request.text)

    if await edit_tariff_data_controller(request, state):
        return

    return await insert_tariff_data(request, state)
