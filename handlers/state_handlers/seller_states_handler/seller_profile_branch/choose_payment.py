import importlib
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from states.tariffs_to_seller import ChoiceTariffForSellerStates
from utils.Lexicon import LexiconChoicePaymentSystem

async def payments_lexicon_part_constructor():
    '''Конструктор lexicon_part'a для предоставления выбора оплат'''
    lexicon_part = dict()
    lexicon_part['message_text'] = LexiconChoicePaymentSystem.message_text
    lexicon_part['buttons'] = {
        callback_data: caption for button_pare in LexiconChoicePaymentSystem.buttons_list
                                for callback_data, caption in button_pare.items()
                                 }
    return lexicon_part

async def choice_payments_handler(callback: CallbackQuery, state: FSMContext):
    '''Обработчик предоставления выбора системы оплаты для покупки тарифа'''
    message_editor_module = importlib.import_module('handlers.message_editor')

    lexicon_part = await payments_lexicon_part_constructor()

    memory_data = await state.get_data()
    need_tariff_id = memory_data.get('current_tariff_id')

    await state.set_state(ChoiceTariffForSellerStates.choose_payment_method)
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)
