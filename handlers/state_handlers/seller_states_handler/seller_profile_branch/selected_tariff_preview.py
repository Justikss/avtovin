from aiogram.types import CallbackQuery
import importlib
from aiogram.fsm.context import FSMContext

from states.tariffs_to_seller import ChoiceTariffForSellerStates
from utils.lexicon_utils.Lexicon import LexiconSelectedTariffPreview, LEXICON
from utils.get_currency_sum_usd import convertator


async def tariff_preview_card_constructor(tariff_id) -> dict:
    '''Метод структурирует данные тарифа с кнопками в lexicon_part по которому выводится блок
    сообщения с теми же кнопками'''
    tariff_request_module = importlib.import_module('database.data_requests.tariff_requests')
    tariff_model = await tariff_request_module.TarifRequester.get_by_id(tariff_id=tariff_id)

    print('TID ', tariff_id)
    price = f'''{await convertator('sum', tariff_model.price)}$ {LEXICON['convertation_sub_string']} {LEXICON['uzbekistan_valute'].replace('X', str(tariff_model.price))}'''
    tariff_view_card = f'''\
        {LexiconSelectedTariffPreview.header}\n\
{LexiconSelectedTariffPreview.separator}\
        {LexiconSelectedTariffPreview.name.replace('X', tariff_model.name)}\
            {LexiconSelectedTariffPreview.low_separator}\
                {LexiconSelectedTariffPreview.duration_time.replace('X', str(tariff_model.duration_time))}\
            {LexiconSelectedTariffPreview.low_separator}\
                    {LexiconSelectedTariffPreview.feedback_amount.replace('X', str(tariff_model.feedback_amount))}\
            {LexiconSelectedTariffPreview.low_separator}\
                    {LexiconSelectedTariffPreview.price.replace('X', price)}\
{LexiconSelectedTariffPreview.separator}\
                    '''

    lexicon_part = {'message_text': tariff_view_card, 'buttons': LexiconSelectedTariffPreview.buttons}

    return lexicon_part

async def tariff_preview_handler(callback: CallbackQuery, state: FSMContext, backward_call=False):
    '''Обработчик кнопки для вывода информации по выбранному тарифу'''
    message_editor_module = importlib.import_module('handlers.message_editor')
    memory_bag_dixer_module = importlib.import_module('utils.memory_bagfixer')
    print('BW', backward_call)
    if not backward_call:
        print('NBC')
        tariff_id = callback.data.split(':')[-1]
        await state.update_data(current_tariff_id=tariff_id)
    else:
        print("YBC")
        memory_storage = await state.get_data()
        tariff_id = memory_storage.get('current_tariff_id')
        print(tariff_id)
        if not tariff_id:
            await memory_bag_dixer_module.memory_was_lost(callback=callback, mode='seller')

    lexicon_part = await tariff_preview_card_constructor(tariff_id=tariff_id)
    await state.set_state(ChoiceTariffForSellerStates.preview_tariff)
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)
