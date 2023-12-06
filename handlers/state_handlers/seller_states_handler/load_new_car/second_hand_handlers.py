import logging
from typing import Union

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import importlib

from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.new_car_photo_requests import PhotoRequester

from utils.Lexicon import LexiconCommodityLoader
from states.load_commodity_states import LoadCommodityStates
from utils.create_lexicon_part import create_lexicon_part


async def input_year_to_load(callback: CallbackQuery, state: FSMContext, other_color_mode=False):
    '''Выбрать год добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    rewrite_controller_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.utils')
    memory_storage = await state.get_data()
    if await rewrite_controller_module.rewrite_boot_state_stopper(request=callback, state=state):
        if not callback.data.startswith('rewrite_boot_') and not memory_storage.get('rewrite_state_flag'):
            ic()
            if not other_color_mode:
                await state.update_data(color_for_load=int(callback.data.split('_')[-1]))

    if await rewrite_controller_module.data_update_controller(request=callback, state=state):
        return

    lexicon_part = await create_lexicon_part(lexicon_part_abc=LexiconCommodityLoader.load_commodity_year_of_realise,
                                             buttons_captions=await CarConfigs.get_characteristic(year=True))
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, dynamic_buttons=True)

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
                                             buttons_captions=await CarConfigs.get_characteristic(mileage=True))
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, dynamic_buttons=True)

    await callback.answer()
    # await state.set_state(LoadCommodityStates.input_to_load_color)
    await state.set_state(LoadCommodityStates.input_to_load_price)


