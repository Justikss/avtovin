from aiogram.types import CallbackQuery
import importlib
from aiogram.fsm.context import FSMContext

from states.tariffs_to_seller import ChoiceTariffForSellerStates
from utils.Lexicon import LexiconSelectedTariffPreview, LEXICON


async def tariff_preview_card_constructor(tariff_id) -> dict:
    '''Метод структурирует данные тарифа с кнопками в lexicon_part по которому выводится блок
    сообщения с теми же кнопками'''
    tarif_request_module = importlib.import_module('database.data_requests.tariff_requests')

    print('TID ', tariff_id)
    tariff_model = tarif_request_module.TarifRequester.get_by_id(tariff_id=tariff_id)
    tariff_view_card = f'{LexiconSelectedTariffPreview.header}\
        {LexiconSelectedTariffPreview.name}{tariff_model.name}\
            {LexiconSelectedTariffPreview.price}{tariff_model.price}\
                {LexiconSelectedTariffPreview.duration_time}{tariff_model.duration_time}\
                    {LexiconSelectedTariffPreview.feedback_amount}{tariff_model.feedback_amount}'

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
