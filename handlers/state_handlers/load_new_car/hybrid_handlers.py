from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import importlib

from states.load_commodity_states import LoadCommodityStates
from utils.Lexicon import LexiconCommodityLoader

async def get_load_car_state(state: FSMContext):
    '''Метод-помощник для определения категории состояния авто в обработке FSM'''
    memory_data = await state.get_data()
    cars_state = memory_data.get('state_for_load')

    if cars_state.endswith('second_hand'):
        return 'second_hand'

    elif cars_state.endswith('new'):
        return 'new'


async def input_state_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать состояние добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    
    await state.set_state(LoadCommodityStates.input_to_load_state)

    lexicon_part = LexiconCommodityLoader.load_commodity_state
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)
    
    await state.set_state(LoadCommodityStates.input_to_load_engine_type)


async def input_engine_type_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать двигатель добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await state.update_data(state_for_load=callback.data)
    
    lexicon_part = LexiconCommodityLoader.load_engine_type
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

    await state.set_state(LoadCommodityStates.input_to_load_brand)

async def input_brand_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать марку добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await state.update_data(engine_for_load=callback.data)
    
    lexicon_part = LexiconCommodityLoader.load_commodity_brand
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

    await state.set_state(LoadCommodityStates.input_to_load_model)


async def input_model_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать модель добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    
    await state.update_data(brand_for_load=callback.data)

    lexicon_part = LexiconCommodityLoader.load_commodity_model
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

    await state.set_state(LoadCommodityStates.input_to_load_complectation)


async def input_complectation_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать комплектацию добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    
    await state.update_data(model_for_load=callback.data)
    
    lexicon_part = LexiconCommodityLoader.load_commodity_complectation
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

    cars_state = await get_load_car_state(state=state)
    print('cstate: ', cars_state)
    if cars_state == 'new':
        await state.set_state(LoadCommodityStates.input_to_load_price)

    elif cars_state == 'second_hand':
        await state.set_state(LoadCommodityStates.input_to_load_year)


async def input_price_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать цену добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    
    cars_state = await get_load_car_state(state=state)
    if cars_state == 'new':
        await state.update_data(complectation_for_load=callback.data)

    elif cars_state == 'second_hand':
        await state.update_data(color_for_load=callback.data)
    
    lexicon_part = LexiconCommodityLoader.load_commodity_price
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

    await state.set_state(LoadCommodityStates.input_to_load_photo)


async def input_photo_to_load(message: Message, state: FSMContext):
    '''Вставить фото добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await message.delete()
    await state.update_data(load_price=message.text)

    lexicon_part = LexiconCommodityLoader.load_commodity_photo
    await message_editor.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=lexicon_part)

    await state.set_state(LoadCommodityStates.load_config_output)
