from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import importlib
from typing import Union

from states.load_commodity_states import LoadCommodityStates
from utils.Lexicon import LexiconCommodityLoader, LEXICON

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
    
    # await message_editor.redis_data.set_data(key=str(callback.from_user.id) + ':load_car_state',
    #                                         value=cars_state)


async def input_price_to_load(request: Union[CallbackQuery, Message], state: FSMContext, incorrect=False):
    '''Выбрать цену добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    lexicon_part = LexiconCommodityLoader.load_commodity_price
    print('bpart ', lexicon_part)

    if not incorrect:
        cars_state = await get_load_car_state(state=state)
        if cars_state == 'new':
            await state.update_data(complectation_for_load=request.data)

        elif cars_state == 'second_hand':
            await state.update_data(color_for_load=request.data)
        reply_mode = False
        await state.update_data(incorrect_flag=False)
    else:
        await state.update_data(incorrect_flag=True)
        reply_mode = True
        if lexicon_part['message_text'].endswith(LEXICON['message_not_digit']):
            pass
        else:
            lexicon_part['message_text'] += LEXICON['message_not_digit']
    print('replm: ', reply_mode)

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part, reply_mode=reply_mode, seller_boot=True)

    await state.set_state(LoadCommodityStates.input_to_load_photo)


async def input_photo_to_load(message: Message, state: FSMContext, incorrect=False, car_price=None):
    '''Вставить фото добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    lexicon_part = LexiconCommodityLoader.load_commodity_photo

    delete_mode = False

    if not incorrect:
        memory_storage = await state.get_data()
        if memory_storage['incorrect_flag']:
            delete_mode=True
        await state.update_data(load_price=car_price)
        reply_mode = False
        await state.update_data(incorrect_flag=False)
    else:
        await state.update_data(incorrect_flag=True)
        reply_mode  = True
        if lexicon_part['message_text'].startswith(LEXICON['message_not_photo']):
            pass
        else:
            print(lexicon_part)
            print(LEXICON['message_not_photo'])
            new_lexicon_part = {'message_text': LEXICON['message_not_photo']}
            for key, value in lexicon_part['buttons'].items():
                new_lexicon_part[key] = value

    await message_editor.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=new_lexicon_part, reply_mode=reply_mode, seller_boot=True, delete_mode=delete_mode)

    await state.set_state(LoadCommodityStates.load_config_output)
