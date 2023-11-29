from copy import copy

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import importlib
from typing import Union
from icecream import ic

from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.new_car_photo_requests import PhotoRequester
from states.load_commodity_states import LoadCommodityStates
from utils.Lexicon import LexiconCommodityLoader, LEXICON
from handlers.state_handlers.seller_states_handler.load_new_car.utils import data_update_controller, change_boot_car_state_controller, rewrite_boot_state_stopper
from utils.create_lexicon_part import create_lexicon_part


async def get_load_car_state(state: FSMContext):
    '''Метод-помощник для определения категории состояния авто в обработке FSM'''
    memory_data = await state.get_data()
    cars_state = memory_data.get('state_for_load')

    print('cstte: ', cars_state)

    if cars_state == 2:
        return 'second_hand'

    elif cars_state == 1:
        return 'new'


async def input_state_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать состояние добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    if not bot:
        bot = callback.message.bot
    await state.set_state(LoadCommodityStates.input_to_load_state)

    if callback.data.startswith('rewrite_boot_'):
        delete_mode = True
    else:
        delete_mode = False

    lexicon_part = await create_lexicon_part(lexicon_part_abc=LexiconCommodityLoader.load_commodity_state,
                                             buttons_captions=await CarConfigs.get_all_states())
    ic(lexicon_part)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, bot=bot, delete_mode=delete_mode)

    await callback.answer()
    await state.set_state(LoadCommodityStates.input_to_load_engine_type)


async def input_engine_type_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать двигатель добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    if not bot:
        bot = callback.message.bot

    if not callback.data.startswith('rewrite_boot_'):
        await change_boot_car_state_controller(callback, state)

        await state.update_data(state_for_load=int(callback.data.split('_')[-1]))
    if await data_update_controller(request=callback, state=state):
        return

    lexicon_part = await create_lexicon_part(lexicon_part_abc=LexiconCommodityLoader.load_engine_type,
                                             buttons_captions=await CarConfigs.get_all_engines())
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, bot=bot)

    await callback.answer()
    await state.set_state(LoadCommodityStates.input_to_load_brand)

async def input_brand_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать марку добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    if not bot:
        bot = callback.message.bot

    if not callback.data.startswith('rewrite_boot_'):
        await state.update_data(engine_for_load=int(callback.data.split('_')[-1]))
    if await data_update_controller(request=callback, state=state):
        return

    lexicon_part = await create_lexicon_part(lexicon_part_abc=LexiconCommodityLoader.load_commodity_brand,
                                             buttons_captions=await CarConfigs.get_all_brands())
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, bot=bot)

    await callback.answer()
    await state.set_state(LoadCommodityStates.input_to_load_model)


async def input_model_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать модель добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    if not bot:
        bot = callback.message.bot

    data_update_result = await data_update_controller(request=callback, state=state)

    if not callback.data.startswith('rewrite_boot_'):
        await state.update_data(brand_for_load=int(callback.data.split('_')[-1]))
        brand_for_load = int(callback.data.split('_')[-1])
    else:
        memory_storage = await state.get_data()
        brand_for_load = memory_storage['brand_for_load']

    if data_update_result:
        return

    lexicon_part = await create_lexicon_part(lexicon_part_abc=LexiconCommodityLoader.load_commodity_model,
                                             buttons_captions=await CarConfigs.get_models_by_brand(brand_for_load))
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, bot=bot)

    await callback.answer()
    await state.set_state(LoadCommodityStates.input_to_load_complectation)


async def input_complectation_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать комплектацию добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    
    if not bot:
        bot = callback.message.bot


    data_update_result = await data_update_controller(request=callback, state=state)

    if not callback.data.startswith('rewrite_boot_'):
        await state.update_data(model_for_load=int(callback.data.split('_')[-1]))
        model_for_load = int(callback.data.split('_')[-1])
    else:
        memory_storage = await state.get_data()
        model_for_load = memory_storage['model_for_load']

    if data_update_result:
        return

    lexicon_part = await create_lexicon_part(lexicon_part_abc=LexiconCommodityLoader.load_commodity_complectation,
                                             buttons_captions=await CarConfigs.get_complectations_by_model(
                                                 model_for_load))
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, bot=bot)

    cars_state = await get_load_car_state(state=state)
    print('cstate: ', cars_state)
    if cars_state == 'new':
        await state.set_state(LoadCommodityStates.input_to_load_price)

    elif cars_state == 'second_hand':
        await state.set_state(LoadCommodityStates.input_to_load_year)

    await callback.answer()


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
        data_update_result = await data_update_controller(request=request, state=state)

        if not request.data.startswith('rewrite_boot_'):
            cars_state = await get_load_car_state(state=state)
            if cars_state == 'new':
                await state.update_data(complectation_for_load=int(request.data.split('_')[-1]))

            elif cars_state == 'second_hand':
                await state.update_data(color_for_load=int(request.data.split('_')[-1]))


        if data_update_result:
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

    if isinstance(request, CallbackQuery):
        await request.answer()

    await state.set_state(LoadCommodityStates.input_to_load_photo)



