from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

from config_data.config import tariffs_pagesize
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler import output_choose
from utils.lexicon_utils.Lexicon import LexiconTariffSelection
from states.tariffs_to_seller import ChoiceTariffForSellerStates
from utils.user_notification import try_delete_notification


async def output_affordable_tariffs(callback, state):
    '''Метод структурирует своеобразный 'Мок' lexicon_part'a по которому выводится блок сообщения с кнопками'''
    tarif_request_module = importlib.import_module('database.data_requests.tariff_requests')
    
    affordable_tariffs = await tarif_request_module.TarifRequester.retrieve_all_data()
    if not affordable_tariffs:
        return False

    lexicon_class = LexiconTariffSelection

    await state.set_state(ChoiceTariffForSellerStates.choose_tariff)
    await output_choose(callback, state, lexicon_class, affordable_tariffs, tariffs_pagesize)

    return affordable_tariffs


async def output_affordable_tariffs_handler(callback: CallbackQuery, state: FSMContext):
    '''Обработчик кнопки ПРОДЛИТЬ ТАРИФ
    Предоставляет список всех доступных тарифов'''
    await try_delete_notification(callback, user_status='lose_tariff')
    lexicon_part = await output_affordable_tariffs(callback, state)
    
    if not lexicon_part:
        await callback.answer(LexiconTariffSelection.not_found_message_text)
