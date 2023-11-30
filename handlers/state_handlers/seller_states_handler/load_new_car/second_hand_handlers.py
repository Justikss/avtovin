from typing import Union

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import importlib

from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.new_car_photo_requests import PhotoRequester

from utils.Lexicon import LexiconCommodityLoader
from states.load_commodity_states import LoadCommodityStates
from utils.create_lexicon_part import create_lexicon_part


async def input_year_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать год добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    rewrite_controller_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.utils')
    if await rewrite_controller_module.rewrite_boot_state_stopper(request=callback, state=state):
        if not callback.data.startswith('rewrite_boot_'):
            await state.update_data(complectation_for_load=int(callback.data.split('_')[-1]))
    
    if await rewrite_controller_module.data_update_controller(request=callback, state=state):
        return

    lexicon_part = await create_lexicon_part(lexicon_part_abc=LexiconCommodityLoader.load_commodity_year_of_realise,
                                             buttons_captions=await CarConfigs.get_for_second_hand(year=True))
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

    await callback.answer()
    await state.set_state(LoadCommodityStates.input_to_load_mileage)


async def input_mileage_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать пробег добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    rewrite_controller_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')

    if not callback.data.startswith('rewrite_boot_'):
        await state.update_data(year_for_load=int(callback.data.split('_')[-1]))
    if await rewrite_controller_module.data_update_controller(request=callback, state=state):
        return

    lexicon_part = await create_lexicon_part(lexicon_part_abc=LexiconCommodityLoader.load_commodity_mileage,
                                             buttons_captions=await CarConfigs.get_for_second_hand(mileage=True))
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

    await callback.answer()
    await state.set_state(LoadCommodityStates.input_to_load_color)


async def input_color_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать цвет добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    rewrite_controller_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')
    if not callback.data.startswith('rewrite_boot_'):
        await state.update_data(mileage_for_load=int(callback.data.split('_')[-1]))
    if await rewrite_controller_module.data_update_controller(request=callback, state=state):
        return

    lexicon_part = await create_lexicon_part(lexicon_part_abc=LexiconCommodityLoader.load_commodity_color,
                                             buttons_captions=await CarConfigs.get_for_second_hand(color=True))
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)

    await callback.answer()
    await state.set_state(LoadCommodityStates.input_to_load_price)

async def input_photo_to_load(request: Union[CallbackQuery, Message], state: FSMContext, incorrect=False, car_price=None, bot=None, reply_mode=False):
    '''Вставить фото добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    rewrite_controller_module = importlib.import_module(
        'handlers.state_handlers.seller_states_handler.load_new_car.utils')

    lexicon_part = LexiconCommodityLoader.load_commodity_photo
    if not bot:
        if isinstance(request, CallbackQuery):
            bot = request.message.bot
        else:
            bot = request.bot

    delete_mode = False

    incorrect_notification = lexicon_part['message_text'].split("\n")[3]
    lexicon_part['message_text'] = lexicon_part['message_text'].split('\n')
    print('lexicon_part0', lexicon_part)
    lexicon_part['message_text'][3] = f'<b>{incorrect_notification}</b>'
    print('lexicon_part1', lexicon_part)
    print(incorrect_notification)
    lexicon_part['message_text'] = '\n'.join(lexicon_part['message_text'])
    print('lexicon_part2', lexicon_part)

    if not incorrect:
        memory_storage = await state.get_data()
        if memory_storage.get('incorrect_flag'):
            delete_mode = True
        if car_price != None:
            get_load_car_state_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')

            ic(car_price)

            await state.update_data(load_price=int(car_price))
            cars_state = await get_load_car_state_module.get_load_car_state(state=state)
            print('cstate: ', cars_state)
            if cars_state == 'new':
                output_config_module = importlib.import_module(
                    'handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs')
            #
            #
            #     photo_pack = await PhotoRequester.try_get_photo(state)
            #     ic(photo_pack)
                await output_config_module.output_load_config_for_seller(request, state)
                return

        if await rewrite_controller_module.data_update_controller(request=request, state=state):
            return

        await state.update_data(incorrect_flag=False)
        incorrect_flag = False
    else:
        await state.update_data(incorrect_flag=True)
        incorrect_flag = True
        ic(request.photo)
        if not request.photo:
            await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                            bot=bot, delete_mode=delete_mode, reply_message=request.message_id)

    if (isinstance(request, Message) and request.photo) or not incorrect_flag:
        await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,  bot=bot, delete_mode=delete_mode)
    await state.update_data(rewrite_state_flag=None)

    if isinstance(request, CallbackQuery):
        await request.answer()
    await state.set_state(LoadCommodityStates.photo_verification)
