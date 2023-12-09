import asyncio
from copy import copy

from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from typing import Union
import importlib

from config_data.config import money_valute
from database.data_requests.new_car_photo_requests import PhotoRequester
from states.load_commodity_states import LoadCommodityStates
from handlers.state_handlers.seller_states_handler.load_new_car.load_data_fromatter import data_formatter
from utils.get_currency_sum_usd import get_valutes
from utils.lexicon_utils.Lexicon import LexiconSellerRequests as Lexicon, LEXICON


async def get_output_string(mode, boot_data: dict) -> str:
    '''Метод создаёт строку для вывода выбранных конфигураций загружаемого авто продавцу/админам.'''
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')

    if mode == 'to_seller':
        start_sub_string = copy(lexicon_module.LexiconCommodityLoader.config_for_seller)
    elif mode.startswith('to_admins_from_'):
        seller_link = mode.split('_')[3]
        start_sub_string = copy(lexicon_module.LexiconCommodityLoader.config_for_admins).replace('X', seller_link)

    block_string = await get_valutes(boot_data.get('dollar_price'), boot_data.get('sum_price'), get_string='block')

    bottom_layer = f'''\
    \n{LEXICON['confirm_from_seller']['message_text']['separator']}\
    \n{block_string}\
    \n{boot_data.get('photo_id')}\n{boot_data.get('photo_unique_id')}'''

    top_layer = f'''{start_sub_string}\
    \n{LEXICON['confirm_from_seller']['message_text']['separator']}\
          {copy(Lexicon.commodity_state).replace('X', boot_data['state'])}\
          {copy(Lexicon.engine_type).replace('X', boot_data['engine_type'])}\
          {copy(Lexicon.commodity_brand).replace('X', boot_data['brand'])}\
          {copy(Lexicon.commodity_model).replace('X', boot_data['model'])}\
          {copy(Lexicon.commodity_complectation).replace('X', boot_data['complectation'])}\
          {copy(Lexicon.commodity_color).replace('X', boot_data['color'])}'''

    is_second_hand = (boot_data['year_of_release'], boot_data['mileage'])
    if None not in is_second_hand:
        middle_layer = f'''{copy(Lexicon.commodity_year_of_realise).replace('X', boot_data['year_of_release'])}\
              {copy(Lexicon.commodity_mileage).replace('X', boot_data['mileage'])}'''
        output_load_commodity_config = top_layer + middle_layer + bottom_layer
    else:
        output_load_commodity_config = top_layer + bottom_layer

    return output_load_commodity_config

mediagroups = {}

async def output_load_config_for_seller(request: Union[Message, CallbackQuery], state: FSMContext, media_photos=None, need_photo_flag=None, bot=None, structured_boot_data=None):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    create_buttons_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.utils')
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')

    get_load_car_state_module = importlib.import_module(
        'handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')
    if isinstance(request, Message):
        message = request
    else:
        message = request.message
    ic(media_photos)
    memory_storage = await state.get_data()
    await state.update_data(other_color_mode=False)
    await state.update_data(rewrite_state_flag=None)
    await state.update_data(rewrite_brand_mode=False)
    cars_state = await get_load_car_state_module.get_load_car_state(state=state)
    print('cstate: ', cars_state)
    if cars_state == 'new':
        output_config_module = importlib.import_module(
            'handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs')

        photo_pack = await PhotoRequester.try_get_photo(state)
        ic(photo_pack)
        if photo_pack:
            media_photos=photo_pack
        else:
            if (not memory_storage.get('load_photo') and not media_photos) or need_photo_flag:
                input_photo_module = importlib.import_module(
                    'handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')
                ic()
                ic(need_photo_flag, memory_storage.get('load_photo'), media_photos)
                ic(True)
                return await input_photo_module.input_photo_to_load(request, state, need_photo_flag=True)
            # await state.update_data(load_photo=photo_pack)

    memory_storage = await state.get_data()
    if memory_storage.get('incorrect_flag'):
        try:
            message_id = await message_editor.redis_data.get_data(key=f'{request.from_user.id}:last_seller_message')
            if message_id:
                await message.chat.delete_message(message_id=message_id)
            await state.update_data(incorrect_flag=False)
        except:
            pass

        await message_editor.redis_data.delete_key(key=f'{request.from_user.id}:last_seller_message')

    if media_photos:
        await state.update_data(load_photo=media_photos)

    if not bot:
        if isinstance(request, Message):
            # await request.delete()
            bot = request.bot
        else:
            bot = request.message.bot

    if memory_storage.get('incorrect_flag'):
        delete_mode = True
    else:
        delete_mode = False


    if not structured_boot_data:
        structured_boot_data = await data_formatter(request=request, state=state)
        await message_editor.redis_data.set_data(key=f'{str(request.from_user.id)}:structured_boot_data',
                                                 value = structured_boot_data)


    output_string = await get_output_string(mode='to_seller',
                                            boot_data=structured_boot_data)

    await message_editor.redis_data.set_data(key=str(request.from_user.id) + ':boot_config', value=output_string)
    ic(output_string)
    # output_string = '\n'.join(output_string.split('\n')[:-2])
    # ic(output_string)
    output_string = output_string.replace('None', '').strip()
    # output_string += copy(lexicon_module.LexiconCommodityLoader.can_rewrite_config)
    ic(output_string)

    lexicon_part = await create_buttons_module.create_edit_buttons_for_boot_config(state=state, boot_data=structured_boot_data, output_string=output_string, )
    print('lp: ', lexicon_part)

    await message_editor.redis_data.set_data(key=str(request.from_user.id) + ':can_edit_seller_boot_commodity', value=True)

    print('photo_exist?output: ', structured_boot_data.get('photos'))
    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                    media_group=structured_boot_data.get('photos'),
                                                    delete_mode=delete_mode,
                                                    seller_boot=True, bot=bot)

    if isinstance(request, CallbackQuery):
        await request.answer()

    await state.set_state(LoadCommodityStates.load_config_output)