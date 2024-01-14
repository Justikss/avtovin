from copy import copy

from aiogram.types import CallbackQuery
import importlib
from aiogram.fsm.context import FSMContext

from states.tariffs_to_seller import ChoiceTariffForSellerStates
from utils.get_currency_sum_usd import convertator
from utils.lexicon_utils.Lexicon import class_lexicon

admin_lexicon_module = importlib.import_module('utils.lexicon_utils.admin_lexicon.admin_lexicon')

async def tariff_preview_card_constructor(tariff_id, by_admin=False, by_admin_tariff=False) -> dict:
    '''Метод структурирует данные тарифа с кнопками в lexicon_part по которому выводится блок
    сообщения с теми же кнопками'''
    tariff_request_module = importlib.import_module('database.data_requests.tariff_requests')
    Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    tariff_model = await tariff_request_module.TarifRequester.get_by_id(tariff_id=tariff_id)
    ic(tariff_model.name)
    lexicon_class = copy(Lexicon_module.LexiconSelectedTariffPreview)
    price = f'''{await convertator('sum', tariff_model.price)}$ {Lexicon_module.LEXICON['convertation_sub_string']} {Lexicon_module.LEXICON['uzbekistan_valute'].replace('X', str(tariff_model.price))}'''
    tariff_view_card = f'''\
        {lexicon_class.header}\n\
{lexicon_class.separator}\
{lexicon_class.tariff_block.format(tariff_name=tariff_model.name, days_remaining=tariff_model.duration_time, 
                                   feedbacks_remaining=tariff_model.feedback_amount)}\
{lexicon_class.separator}{class_lexicon['tariff_price'].format(tariff_price=price)}'''

    if by_admin:
        buttons = copy(admin_lexicon_module.ChooseTariff.tariff_review_buttons)
    elif by_admin_tariff:
        buttons = Lexicon_module.ADMIN_LEXICON['tariff_view_buttons']
    else:
        buttons = lexicon_class.buttons
    lexicon_part = {'message_text': tariff_view_card, 'buttons': buttons}

    return lexicon_part

async def tariff_preview_handler(callback: CallbackQuery, state: FSMContext, backward_call=False):
    '''Обработчик кнопки для вывода информации по выбранному тарифу'''
    message_editor_module = importlib.import_module('handlers.message_editor')
    memory_bag_dixer_module = importlib.import_module('utils.memory_bagfixer')
    if not backward_call:
        tariff_id = callback.data.split(':')[-1]
        await state.update_data(current_tariff_id=tariff_id)
    else:
        memory_storage = await state.get_data()
        tariff_id = memory_storage.get('current_tariff_id')
        if not tariff_id:
            await memory_bag_dixer_module.memory_was_lost(callback=callback, mode='seller')

    lexicon_part = await tariff_preview_card_constructor(tariff_id=tariff_id)
    await state.set_state(ChoiceTariffForSellerStates.preview_tariff)
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)
