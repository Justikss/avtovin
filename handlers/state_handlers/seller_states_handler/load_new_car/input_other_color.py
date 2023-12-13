import importlib
from copy import copy
from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.new_car_photo_requests import PhotoRequester
from handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers import get_load_car_state, \
    input_price_to_load
from handlers.state_handlers.seller_states_handler.load_new_car.second_hand_handlers import input_year_to_load
from states.load_commodity_states import LoadCommodityStates
from utils.lexicon_utils.commodity_loader import LexiconCommodityLoader


async def delete_last_user_message(message: Message):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    last_message = await message_editor.redis_data.get_data(key=f'{str(message.from_user.id)}:last_seller_message')
    if last_message:
        try:
            await message.chat.delete_message(last_message)
        except:
            pass


async def input_other_color_to_boot_car(request: Union[CallbackQuery, Message], state: FSMContext, incorrect=False):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    lexicon_part = copy(LexiconCommodityLoader.load_other_color)
    if incorrect:
        lexicon_part['message_text'] = f'''{lexicon_part['message_text']}{copy(LexiconCommodityLoader.load_other_color_incorrect_message_text)}'''
        # reply_message = await message_editor.redis_data.get_data(key=f'{str(request.from_user.id)}:last_seller_message')
        reply_mode=True

    else:
        await state.set_state(LoadCommodityStates.input_other_color)
        reply_mode = False
    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part, reply_mode=reply_mode, delete_mode=incorrect)

async def validate_other_color(message: Message, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    incorrect_flag = None
    await delete_last_user_message(message)

    if message.text.isalpha() or message.text.replace('-', '').isalpha():
        memory_storage = await state.get_data()
        correct_answer = message.text.capitalize()

        try:
            await message.delete()
        except:
            pass

        match_check_status = await CarConfigs.get_colors_by_name(color_name=correct_answer)

        if not match_check_status:
            color_value = correct_answer
        else:
            color_value = match_check_status[0].id

        await state.update_data(color_to_pre_load=color_value)
        if memory_storage.get('incorrect_flag'):
            await state.update_data(incorrect_flag=False)
            delete_mode = True
        else:
            delete_mode = False

        lexicon_part = copy(LexiconCommodityLoader.make_sure_selected_other_color)
        lexicon_part['message_text'] = lexicon_part['message_text'].replace('X', correct_answer)
        return await message_editor.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=lexicon_part, delete_mode=delete_mode)

    else:
        await state.update_data(incorrect_flag=True)
        await input_other_color_to_boot_car(request=message, state=state, incorrect=True)
        await message_editor.redis_data.set_data(key=f'{str(message.from_user.id)}:last_seller_message', value=message.message_id)

async def success_load_other_color(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    memory_storage = await state.get_data()
    old_color_value = memory_storage.get('color_for_load')
    current_color_value = memory_storage['color_to_pre_load']
    await state.update_data(color_for_load=current_color_value)
    ic(memory_storage.get('color_to_pre_load'))
    await state.update_data(other_color_mode=True)

    cars_state = await get_load_car_state(state=state)

    if cars_state == 'new':
        ic()
        ic(cars_state)
        ic(old_color_value, current_color_value)
        if old_color_value:
            if str(old_color_value) != str(current_color_value):
                input_photo_module = importlib.import_module(
                    'handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')
                if current_color_value.isalpha():
                    need_photo_flag = True
                else:
                    need_photo_flag = False
                ic()
                print('input_photo_to_load')#
                if not (str(old_color_value).isalpha() and str(current_color_value).isalpha()):
                    return await input_photo_module.input_photo_to_load(callback, state, need_photo_flag=need_photo_flag)#
        await state.set_state(LoadCommodityStates.input_to_load_price)
        print('go_to_price')
        await input_price_to_load(callback, state, other_color_mode=True)
        # await state.set_state(LoadCommodityStates.input_to_load_color)
    elif cars_state == 'second_hand':
        await state.set_state(LoadCommodityStates.input_to_load_year)
        await input_year_to_load(callback, state, other_color_mode=True)
