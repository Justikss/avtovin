from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import importlib
from typing import Union

from states.load_commodity_states import LoadCommodityStates
from utils.Lexicon import LexiconCommodityLoader, LEXICON
from handlers.state_handlers.seller_states_handler.load_new_car.utils import data_update_controller, change_boot_car_state_controller, rewrite_boot_state_stopper


async def get_load_car_state(state: FSMContext):
    '''Метод-помощник для определения категории состояния авто в обработке FSM'''
    memory_data = await state.get_data()
    cars_state = memory_data.get('state_for_load')
    print('cstte: ', cars_state)

    if cars_state.endswith('second_hand'):
        return 'second_hand'

    elif cars_state.endswith('new'):
        return 'new'


async def input_state_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать состояние добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    if not bot:
        bot = callback.message.bot
    await state.set_state(LoadCommodityStates.input_to_load_state)

    lexicon_part = LexiconCommodityLoader.load_commodity_state
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, bot=bot)
    
    await state.set_state(LoadCommodityStates.input_to_load_engine_type)


async def input_engine_type_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать двигатель добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    if not bot:
        bot = callback.message.bot

    if not callback.data.startswith('rewrite_boot_'):
        await change_boot_car_state_controller(callback, state)

        await state.update_data(state_for_load=callback.data)
    if await data_update_controller(request=callback, state=state):
        return

    lexicon_part = LexiconCommodityLoader.load_engine_type
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, bot=bot)

    await state.set_state(LoadCommodityStates.input_to_load_brand)

async def input_brand_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать марку добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    if not bot:
        bot = callback.message.bot

    if not callback.data.startswith('rewrite_boot_'):
        await state.update_data(engine_for_load=callback.data)
    if await data_update_controller(request=callback, state=state):
        return
    
    lexicon_part = LexiconCommodityLoader.load_commodity_brand
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, bot=bot)

    await state.set_state(LoadCommodityStates.input_to_load_model)


async def input_model_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать модель добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    if not bot:
        bot = callback.message.bot

    if not callback.data.startswith('rewrite_boot_'):
        await state.update_data(brand_for_load=callback.data)
    if await data_update_controller(request=callback, state=state):
        return

    lexicon_part = LexiconCommodityLoader.load_commodity_model
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, bot=bot)

    await state.set_state(LoadCommodityStates.input_to_load_complectation)


async def input_complectation_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать комплектацию добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    
    if not bot:
        bot = callback.message.bot

    memory_data = await state.get_data()
    #if memory_data.get('state_for_load') == :
        
    if not callback.data.startswith('rewrite_boot_'):
        await state.update_data(model_for_load=callback.data)
    if await data_update_controller(request=callback, state=state):
        return
    

    lexicon_part = LexiconCommodityLoader.load_commodity_complectation
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, bot=bot)

    cars_state = await get_load_car_state(state=state)
    print('cstate: ', cars_state)
    if cars_state == 'new':
        await state.set_state(LoadCommodityStates.input_to_load_price)

    elif cars_state == 'second_hand':
        await state.set_state(LoadCommodityStates.input_to_load_year)
    
    # await message_editor.redis_data.set_data(key=str(callback.from_user.id) + ':load_car_state',
    #                                         value=cars_state)


async def input_price_to_load(request: Union[CallbackQuery, Message], state: FSMContext, incorrect=False, bot=None):
    '''Выбрать цену добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    if not bot:
        if isinstance(request, CallbackQuery):
            bot = request.message.bot
        else:
            bot = request.bot

    lexicon_part = None
    print('bpart ', lexicon_part)

    if not incorrect:
        if not request.data.startswith('rewrite_boot_'):
            cars_state = await get_load_car_state(state=state)
            if cars_state == 'new':
                await state.update_data(complectation_for_load=request.data)

            elif cars_state == 'second_hand':
                await state.update_data(color_for_load=request.data)

        if await data_update_controller(request=request, state=state):
            return
        
        reply_mode = False
        await state.update_data(incorrect_flag=False)
    else:
        await state.update_data(incorrect_flag=True)
        reply_mode = True

        lexicon_part = LEXICON['message_not_digit']

    if not lexicon_part:
        lexicon_part = LexiconCommodityLoader.load_commodity_price

    print('replm: ', reply_mode)

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part, reply_mode=reply_mode, seller_boot=True, bot=bot)

    await state.set_state(LoadCommodityStates.input_to_load_photo)


async def input_photo_to_load(request: Union[CallbackQuery, Message], state: FSMContext, incorrect=False, car_price=None, bot=None):
    '''Вставить фото добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    print('load_photo_start')
    lexicon_part = LexiconCommodityLoader.load_commodity_photo
    if not bot:
        if isinstance(request, CallbackQuery):
            bot = request.message.bot
        else:
            bot = request.bot

    delete_mode = False

    if not incorrect:
        memory_storage = await state.get_data()
        if memory_storage.get('incorrect_flag'):
            delete_mode = True
        if car_price != None:
            await state.update_data(load_price=car_price)
        if await data_update_controller(request=request, state=state):
            return

        reply_mode = False
        await state.update_data(incorrect_flag=False)
        new_lexicon_part = lexicon_part
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

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=new_lexicon_part,  bot=bot, delete_mode=delete_mode)
    await state.update_data(rewrite_state_flag=None)
    print('load_photo_end')

    await state.set_state(LoadCommodityStates.photo_verification)
