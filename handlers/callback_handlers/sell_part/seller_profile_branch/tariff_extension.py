from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

from utils.Lexicon import LexiconTariffSelection
from states.tariffs_to_seller import ChoiceTariffForSellerStates

async def lexicon_part_constructor():
    '''Метод структурирует своеобразный 'Мок' lexicon_part'a по которому выводится блок сообщения с кнопками'''
    tarif_request_module = importlib.import_module('database.data_requests.tariff_requests')
    
    affordable_tariffs = tarif_request_module.TarifRequester.retrieve_all_data()
    affordable_tariffs = {tariff.id: tariff.name for tariff in affordable_tariffs}
    lexicon_part = {'message_text': LexiconTariffSelection.message_text, 'buttons': {LexiconTariffSelection.callback_type + str(tariff_id): tariff_name
                             for tariff_id, tariff_name in affordable_tariffs.items()}}

    lexicon_part['buttons'][LexiconTariffSelection.backward_button_callback] = LexiconTariffSelection.backward_button_caption
    lexicon_part['buttons']['width'] = LexiconTariffSelection.keyboard_width_value
    
    print('tsb: ', lexicon_part)
    return lexicon_part


async def output_affordable_tariffs_handler(callback: CallbackQuery, state: FSMContext):
    '''Обработчик кнопки ПРОДЛИТЬ ТАРИФ
    Предоставляет список всех доступных тарифов'''
    message_editor_module = importlib.import_module('handlers.message_editor')

    lexicon_part = await lexicon_part_constructor()
    await state.set_state(ChoiceTariffForSellerStates.choose_tariff)
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_part=lexicon_part, lexicon_key='', dynamic_buttons=True)