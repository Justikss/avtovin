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
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.memory_storage_incorrect_controller import \
    get_incorrect_flag
from handlers.utils.delete_message import delete_message
from states.admin_part_states.tariffs_branch_states import TariffAdminBranchStates
from utils.get_currency_sum_usd import convertator

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
# incorrect_adapter_module = importlib.import_module('utils.oop_handlers_engineering.update_handlers.base_objects.utils_objects.incorrect_adapter')

async def delete_incorrect_message(request, state):
    incorrect_flag = await get_incorrect_flag(state)
    ic(incorrect_flag)
    # if incorrect_flag:
    memory_storage = await state.get_data()
    last_admin_answer = memory_storage.get('last_admin_answer')
    ic(last_admin_answer)
    if last_admin_answer:
        await state.update_data(last_admin_answer=None)
        # ic(last_admin_answer)
        await delete_message(request, last_admin_answer)



async def process_tariff_cost(request: types.Message | types.CallbackQuery, state: FSMContext, incorrect=False):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    await delete_incorrect_message(request, state)
    if isinstance(request, types.CallbackQuery) and request.data[-1].isdigit():
        tariff_id = int(request.data.split(':')[-1])
        await state.update_data(specific_tariff_id=tariff_id)

    await state.set_state(TariffAdminBranchStates.write_tariff_cost)

    delete_mode = await get_delete_mode(state, incorrect)
    lexicon_part, reply_to_message = await incorrect_controller(request, state, incorrect, 'input_tariff_cost', Lexicon_module\
                                                                .ADMIN_LEXICON)
    ic()
    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                    delete_mode=delete_mode, reply_message=reply_to_message)


# Обработчик для записи стоимости тарифа
# @dp.message_handler(lambda message: message.text.isdigit(), state=TariffAdminBranchStates.write_tariff_cost)
async def process_write_tariff_cost(request: types.Message | types.CallbackQuery, state: FSMContext, incorrect=False,
                                    price=None, head_valute=None):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    await delete_incorrect_message(request, state)
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
    lexicon_part, reply_to_message = await incorrect_controller(request, state, incorrect, 'input_tariff_feedbacks', Lexicon_module\
                                                                .ADMIN_LEXICON)
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
    await delete_incorrect_message(request, state)
    if isinstance(request, types.Message) and not incorrect:
        await state.update_data(tariff_feedbacks_residual=int(request.text))

    if await edit_tariff_data_controller(request, state, incorrect):
        return

    lexicon_key = 'input_tariff_time_duration'

    await state.set_state(TariffAdminBranchStates.write_tariff_duration_time)

    delete_mode = await get_delete_mode(state, incorrect)
    lexicon_part, reply_to_message = await incorrect_controller(request, state, incorrect, lexicon_key, Lexicon_module\
                                                                .ADMIN_LEXICON)
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
    await delete_incorrect_message(request, state)
    # await incorrect_adapter_module \
    #     .IncorrectAdapter().try_delete_incorrect_message(request, state)

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
    lexicon_part, reply_to_message = await incorrect_controller(request, state, incorrect, lexicon_key, Lexicon_module\
                                                                .ADMIN_LEXICON)
    await message_editor.travel_editor.edit_message(
        request=request, lexicon_key='', lexicon_part=lexicon_part,
        delete_mode=delete_mode if delete_mode else bool(reply_to_message) is True,
        reply_message=reply_to_message
    )

#Фильтр уникальности
async def process_tariff_name(request: types.Message | types.CallbackQuery, state: FSMContext, message_text=None):
    # Здесь мы просто сохраняем ввод названия тарифа и переходим к следующему состоянию
    if isinstance(request, types.Message) and message_text:
        await state.update_data(tariff_name=message_text)

    if await edit_tariff_data_controller(request, state):
        return

    return await insert_tariff_data(request, state)
