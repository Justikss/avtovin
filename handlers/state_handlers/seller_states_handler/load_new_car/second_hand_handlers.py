import logging
from typing import Union

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import importlib

from config_data.config import car_configurations_in_keyboard_page
from database.data_requests.car_configurations_requests import CarConfigs
from states.load_commodity_states import LoadCommodityStates


async def input_year_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать год добавляемого автомобиля'''
    output_choose_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler')
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')
    rewrite_controller_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.utils')
    memory_storage = await state.get_data()
    if await rewrite_controller_module.rewrite_boot_state_stopper(request=callback, state=state):
        if not callback.data.startswith('rewrite_boot_') and not memory_storage.get('rewrite_state_flag'):
            ic()
            if callback.data[-1].isdigit():
                await state.update_data(color_for_load=int(callback.data.split('_')[-1]))

    if await rewrite_controller_module.data_update_controller(request=callback, state=state):
        return
    lexicon_class = lexicon_module.LexiconCommodityLoader.load_commodity_year_of_realise()
    await output_choose_module.output_choose(callback, state, lexicon_class, await CarConfigs.custom_action('year', 'get_*'),
                        car_configurations_in_keyboard_page, need_last_buttons=False)

    # lexicon_part = await create_lexicon_part(lexicon_part_abc=lexicon_class, request=callback, state=state,
    #                                          buttons_captions=await CarConfigs.get_characteristic(year=True))
    # await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, dynamic_buttons=lexicon_class.dynamic_buttons)

    await callback.answer()
    await state.set_state(LoadCommodityStates.input_to_load_mileage)


async def input_mileage_to_load(callback: CallbackQuery, state: FSMContext):
    '''Выбрать пробег добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')
    rewrite_controller_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')
    output_choose_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler')

    if not callback.data.startswith('rewrite_boot_'):
        if callback.data[-1].isdigit():
            await state.update_data(year_for_load=int(callback.data.split('_')[-1]))
    if await rewrite_controller_module.data_update_controller(request=callback, state=state):
        return
    lexicon_class = lexicon_module.LexiconCommodityLoader.load_commodity_mileage()
    await output_choose_module.output_choose(callback, state, lexicon_class, await CarConfigs.custom_action('mileage', 'get_*'),
                        car_configurations_in_keyboard_page, need_last_buttons=False)
    # lexicon_part = await create_lexicon_part(lexicon_part_abc=lexicon_class, request=callback, state=state,
    #                                          buttons_captions=await CarConfigs.get_characteristic(mileage=True))
    # await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, dynamic_buttons=lexicon_class.dynamic_buttons)

    await callback.answer()
    # await state.set_state(LoadCommodityStates.input_to_load_color)
    await state.set_state(LoadCommodityStates.input_to_load_price)


