import asyncio
import logging
from copy import copy

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import importlib
from typing import Union
from icecream import ic

from states.load_commodity_states import LoadCommodityStates
from handlers.state_handlers.seller_states_handler.load_new_car.utils import data_update_controller, change_boot_car_state_controller, rewrite_boot_state_stopper
from utils.create_lexicon_part import create_lexicon_part

config_module = importlib.import_module('database.data_requests.car_configurations_requests')
bot_config_module = importlib.import_module('config_data.config')


async def get_load_car_state(state: FSMContext):
    '''Метод-помощник для определения категории состояния авто в обработке FSM'''
    memory_data = await state.get_data()
    cars_state = memory_data.get('state_for_load')

    if cars_state == 2:
        return 'second_hand'
    elif cars_state == 1:
        return 'new'


async def input_state_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать состояние добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')

    if not bot:
        bot = callback.message.bot
    await state.set_state(LoadCommodityStates.input_to_load_state)

    if callback.data.startswith('rewrite_boot_'):
        delete_mode = True
    else:
        delete_mode = False
    lexicon_class = lexicon_module.LexiconCommodityLoader.load_commodity_state()
    lexicon_part = await create_lexicon_part(lexicon_part_abc=lexicon_class, request=callback, state=state,
                                             buttons_captions=await config_module\
            .CarConfigs.get_all_states(), need_width=True)
    ic(lexicon_part)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part,
                                                    bot=bot, delete_mode=delete_mode,
                                                    dynamic_buttons=lexicon_class.dynamic_buttons)

    await callback.answer()
    await state.set_state(LoadCommodityStates.input_to_load_engine_type)


async def input_engine_type_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать двигатель добавляемого автомобиля'''
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    if not bot:
        bot = callback.message.bot

    if not callback.data.startswith('rewrite_boot_'):
        await change_boot_car_state_controller(callback, state)
        if callback.data[-1].isdigit():
            await state.update_data(state_for_load=int(callback.data.split('_')[-1]))

    else:
        await state.update_data(rewrite_brand_mode=True)

    if await data_update_controller(request=callback, state=state):
        return
    lexicon_class = lexicon_module.LexiconCommodityLoader.load_commodity_engine_type()
    lexicon_part = await create_lexicon_part(lexicon_part_abc=lexicon_class, request=callback, state=state,
                                             buttons_captions=await config_module\
            .CarConfigs.get_all_engines(), need_width=True)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, bot=bot, dynamic_buttons=lexicon_class.dynamic_buttons)

    await callback.answer()
    await state.set_state(LoadCommodityStates.input_to_load_brand)

async def input_brand_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать марку добавляемого автомобиля'''
    output_choose_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler')
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')

    if not bot:
        bot = callback.message.bot

    there_data_update = await message_editor.redis_data.get_data(
        key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')
    memory_storage = await state.get_data()

    if not callback.data.startswith('rewrite_boot_') and callback.data[-1].isdigit():
        if not there_data_update:
            await state.update_data(engine_for_load=int(callback.data.split('_')[-1]))
        engine_for_load = int(callback.data.split('_')[-1])
    else:
        await state.update_data(rewrite_brand_mode=True)
        engine_for_load = memory_storage.get('engine_for_load')
    if await data_update_controller(request=callback, state=state):
        return
    lexicon_class = lexicon_module.LexiconCommodityLoader.load_commodity_brand()
    await output_choose_module.output_choose(callback, state, lexicon_class, await config_module\
            .CarConfigs.get_brands_by_engine_and_state(engine_for_load, memory_storage.get('state_for_load')),
                        bot_config_module\
                                             .car_configurations_in_keyboard_page, need_last_buttons=False,
                                             unique_names_mode=True)

    await callback.answer()
    await state.set_state(LoadCommodityStates.input_to_load_model)


async def input_model_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать модель добавляемого автомобиля'''
    output_choose_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler')
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')

    if not bot:
        bot = callback.message.bot

    there_data_update = await message_editor.redis_data.get_data(
        key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')
    memory_storage = await state.get_data()

    if not callback.data.startswith('rewrite_boot_') and callback.data[-1].isdigit():
        if not there_data_update:
            await state.update_data(brand_for_load=int(callback.data.split('_')[-1]))
        brand_for_load = int(callback.data.split('_')[-1])
    else:
        memory_storage = await state.get_data()
        brand_for_load = memory_storage['brand_for_load']
        await state.update_data(rewrite_brand_mode=True)

    if await data_update_controller(request=callback, state=state):
        return
    engine_for_load = memory_storage.get('engine_for_load')
    lexicon_class = lexicon_module.LexiconCommodityLoader.load_commodity_model()
    await output_choose_module.output_choose(callback, state, lexicon_class, await config_module\
            .CarConfigs.get_models_by_brand_and_engine_and_state(
                                brand_for_load, memory_storage.get('state_for_load'), engine_for_load),
                                bot_config_module\
                                             .car_configurations_in_keyboard_page, need_last_buttons=False,
                                             unique_names_mode=True)

    await callback.answer()
    await state.set_state(LoadCommodityStates.input_to_load_complectation)


async def input_complectation_to_load(callback: CallbackQuery, state: FSMContext, bot=None):
    '''Выбрать комплектацию добавляемого автомобиля'''
    output_choose_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler')
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')
    
    if not bot:
        bot = callback.message.bot

    there_data_update = await message_editor.redis_data.get_data(
        key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')
    memory_storage = await state.get_data()

    if not callback.data.startswith('rewrite_boot_') and callback.data[-1].isdigit():
        if not there_data_update:
            await state.update_data(model_for_load=int(callback.data.split('_')[-1]))
        model_for_load = int(callback.data.split('_')[-1])
    else:
        model_for_load = memory_storage['model_for_load']
        await state.update_data(rewrite_brand_mode=True)

    engine_for_load = memory_storage.get('engine_for_load')
    if await data_update_controller(request=callback, state=state):
        return
    lexicon_class = lexicon_module.LexiconCommodityLoader.load_commodity_complectation()
    await output_choose_module.output_choose(callback, state, lexicon_class, await config_module\
            .CarConfigs.get_complectations_by_model_and_engine_and_state(
        model_for_load, memory_storage.get('state_for_load'), engine_for_load, for_seller=True), bot_config_module\
                                             .car_configurations_in_keyboard_page, need_last_buttons=False,
                                             unique_names_mode=True)

    await state.set_state(LoadCommodityStates.input_to_load_color)
    await callback.answer()

async def input_color_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать цвет добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    rewrite_controller_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')
    output_choose_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler')

    cars_state = await get_load_car_state(state=state)

    there_data_update = await message_editor.redis_data.get_data(
        key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')
    if there_data_update:
        delete_mode = True
    else:
        delete_mode = False
    if not callback.data.startswith('rewrite_boot_') and (callback.data[-1].isdigit() or callback.data[-1] == ']'):
        ic()
        user_answer = callback.data.split('_')[-1]
        if not there_data_update:
            await state.update_data(complectation_for_load=user_answer)
    else:
        ic()
        memory_storage = await state.get_data()
        user_answer = memory_storage.get('complectation_for_load')
    ic(user_answer)
    if await rewrite_controller_module.data_update_controller(request=callback, state=state):
        return

    lexicon_class = lexicon_module.LexiconCommodityLoader.load_commodity_color()
    last_button_key = next(iter(copy(lexicon_class.last_buttons)))
    last_button_value = lexicon_class.last_buttons[last_button_key]
    ic(last_button_key, last_button_value)
    ic(lexicon_class.last_buttons)
    # lexicon_class.last_buttons = {key: value for key, value in lexicon_class.last_buttons.items() if key != last_button_key}
    ic(lexicon_class.last_buttons)
    match cars_state:
        case 'new':
            colors = await config_module\
                    .CarConfigs.get_color_by_complectaiton(complectation_id=user_answer)
        case 'second_hand':
            colors = await config_module.CarConfigs.custom_action('color', 'get_*')

        case _:
            colors = None
    # if colors:
    last_color_value = await config_module \
        .CarConfigs.get_by_id(table='color', model_id=1)

    if not colors:


        colors = [last_color_value]
        need_last_buttons = False
    else:
        # from database.data_requests.utils.set_color_1_in_last_position import set_other_color_on_last_position
        # colors = await set_other_color_on_last_position(colors)
        colors = [color for color in colors if color.id != 1]
        need_last_buttons = {f'{lexicon_module.LexiconCommodityLoader.load_commodity_color().buttons_callback_data}{str(last_color_value.id)}': last_color_value.name}
    await output_choose_module.output_choose(callback, state, lexicon_class, colors,
                                        bot_config_module\
                                             .car_configurations_in_keyboard_page,
                        need_last_buttons=need_last_buttons)
    await callback.answer()

    if cars_state == 'new':
        await state.set_state(LoadCommodityStates.input_to_load_price)
        # await state.set_state(LoadCommodityStates.input_to_load_color)
    elif cars_state == 'second_hand':
        await state.set_state(LoadCommodityStates.input_to_load_year)

async def input_price_to_load(request: Union[CallbackQuery, Message], state: FSMContext, incorrect=False, bot=None):
    '''Выбрать цену добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')
    base_lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    if await state.get_state() != LoadCommodityStates.input_to_load_price:
        await state.set_state(LoadCommodityStates.input_to_load_price)
    message_text = ''

    if not bot:
        if isinstance(request, CallbackQuery):
            bot = request.message.bot
        else:
            bot = request.bot

    lexicon_part = lexicon_module.LexiconCommodityLoader.load_commodity_price()
    ic(lexicon_part)
    lexicon_part.message_text = copy(lexicon_module.LexiconCommodityLoader.input_price)
    ic(lexicon_part.message_text)


    if not incorrect:

        if not request.data.startswith('rewrite_boot_') and request.data[-1].isdigit():
            ic()
            cars_state = await get_load_car_state(state=state)
            ic(cars_state)

            if cars_state == 'new':
                ic()
                # ic('complectation1221', int(request.data.split('_')[-1]))
                if request.data[-1].isdigit():
                    await state.update_data(color_for_load=int(request.data.split('_')[-1]))

            elif cars_state == 'second_hand':
                ic()
                ic(int(request.data.split('_')[-1]))
                # await state.update_data(color_for_load=int(request.data.split('_')[-1]))
                await state.update_data(mileage_for_load=int(request.data.split('_')[-1]))

        if await data_update_controller(request=request, state=state):
            ic()
            return

        reply_mode = False
        await state.update_data(incorrect_flag=False)
    else:
        await state.update_data(incorrect_flag=True)
        reply_mode = True
        if incorrect == '$':
            Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

            message_text = f'''{lexicon_part.message_text}\n{Lexicon_module.class_lexicon['incorrect_price_$']}'''
        else:
            message_text = base_lexicon_module.LEXICON['message_not_digit']

    if not isinstance(lexicon_part, dict):
        await lexicon_part.initializate(request, state)
    ic(lexicon_part.message_text)

    lexicon_part = await lexicon_part.part()
    ic(lexicon_part)
    if message_text:
        lexicon_part['message_text'] = message_text


    ic(await state.get_state())
    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                    reply_mode=reply_mode, seller_boot=True, bot=bot, delete_mode=True)


    await state.set_state(LoadCommodityStates.input_to_load_photo)



async def input_photo_to_load(request: Union[CallbackQuery, Message], state: FSMContext, incorrect=False, price=None, head_valute=None, bot=None, need_photo_flag=False):
    '''Вставить фото добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    rewrite_controller_module = importlib.import_module(
        'handlers.state_handlers.seller_states_handler.load_new_car.utils')
    get_load_car_state_module = importlib.import_module(
        'handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')
    base_lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    ic()
    lexicon_part = copy(lexicon_module.LexiconCommodityLoader.load_commodity_photo())
    await lexicon_part.initializate(request, state)
    if not bot:
        if isinstance(request, CallbackQuery):
            bot = request.message.bot
        else:
            bot = request.bot

    delete_mode = False
    there_data_update = await message_editor.redis_data.get_data(
        key=str(request.from_user.id) + ':can_edit_seller_boot_commodity')

    memory_storage = await state.get_data()
    ic(memory_storage)
    if not incorrect:
        if not there_data_update:
            cached_states = memory_storage.get('boot_car_states_cache')
            if not cached_states:
                cached_states = []
            # cached_states.append('LoadCommodityStates:input_to_load_price')
            await state.update_data(boot_car_states_cache=cached_states)
        memory_storage = await state.get_data()
        if memory_storage.get('incorrect_flag'):
            delete_mode = True
        if None not in (price, head_valute):

            ic(price, head_valute)
            if head_valute == 'sum':
                await state.update_data(sum_price=price)
                await state.update_data(dollar_price=None)
            elif head_valute == 'usd':
                await state.update_data(dollar_price=price)
                await state.update_data(sum_price=None)

        else:
            logging.info(f'{request.from_user.id} ::: Цена не была найдена в input_photo_to_load handler')

        cars_state = await get_load_car_state_module.get_load_car_state(state=state)

        there_data_update = await message_editor.redis_data.get_data(
            key=str(request.from_user.id) + ':can_edit_seller_boot_commodity')

        if cars_state == 'new' and int(memory_storage.get('color_for_load')) != 1 and not need_photo_flag:
            output_config_module = importlib.import_module(
                'handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs')


            need_photo_flag = False
            #
            #
            #     photo_pack = await PhotoRequester.try_get_photo(state)
            #     ic(photo_pack)
            ic()
            ic(True)
            await output_config_module.output_load_config_for_seller(request, state, need_photo_flag=need_photo_flag)
            return

        if not need_photo_flag:
            if await rewrite_controller_module.data_update_controller(request=request, state=state):
                ic()
                return
        ic()
        await state.update_data(incorrect_flag=False)
        incorrect_flag = False
    else:
        incorrect_notification = lexicon_part.message_text.split("\n")[3]
        message_text = lexicon_part.message_text.split('\n')
        message_text[3] = f'<b>{incorrect_notification}</b>'
        lexicon_part = await lexicon_part.part()

        lexicon_part["message_text"] = '\n'.join(message_text)
        if incorrect == 'size':
            lexicon_part['message_text'] = f'''{base_lexicon_module.LEXICON['incorrect_photo_size']}{lexicon_part['message_text']}'''
        await state.update_data(incorrect_flag=True)
        incorrect_flag = True
        ic(request.photo)
        if not request.photo:
            await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                            bot=bot, delete_mode=delete_mode, reply_message=request.message_id)

    if (isinstance(request, Message) and request.photo) or not incorrect_flag:
        if not isinstance(lexicon_part, dict):
            lexicon_part = await lexicon_part.part()
        ic(lexicon_part)
        await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,  bot=bot, delete_mode=delete_mode)
    await state.update_data(rewrite_state_flag=None)


    await state.set_state(LoadCommodityStates.photo_verification)
