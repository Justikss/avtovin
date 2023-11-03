from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import importlib

from utils.Lexicon import LexiconCommodityLoader
from states.load_commodity_states import LoadCommodityStates



async def input_year_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать модель добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    
    await state.update_data(complectation_for_load=callback.data)

    lexicon_part = LexiconCommodityLoader.load_commodity_year_of_realise
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

    await state.set_state(LoadCommodityStates.input_to_load_complectation)
