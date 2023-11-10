from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from typing import Union
import importlib

from utils.Lexicon import LexiconCommodityLoader, LEXICON
from handlers.state_handlers.seller_states_handler.load_new_car.load_data_fromatter import data_formatter


async def get_output_string(mode, boot_data: dict) -> str:
    '''Метод создаёт строку для вывода выбранных конфигураций загружаемого авто продавцу/админам.'''
    if mode == 'to_seller':
        start_sub_string = LexiconCommodityLoader.config_for_seller
    elif mode.startswith('to_admins_from_'):
        seller_link = mode.split('_')[3]
        start_sub_string = LexiconCommodityLoader.config_for_admins + seller_link

    bottom_layer = f'''{LexiconCommodityLoader.load_commodity_price['message_text']}: {boot_data['price']}\
          \n{boot_data.get('photo_id')}\n{boot_data.get('photo_unique_id')}'''

    top_layer = f'''{start_sub_string}\
          \n{LexiconCommodityLoader.load_commodity_state['message_text']}: {boot_data['state']}\
          \n{LexiconCommodityLoader.load_engine_type['message_text']}: {boot_data['engine_type']}\
          \n{LexiconCommodityLoader.load_commodity_brand['message_text']}: {boot_data['brand']}\
          \n{LexiconCommodityLoader.load_commodity_model['message_text']}: {boot_data['model']}\
          \n{LexiconCommodityLoader.load_commodity_complectation['message_text']}: {boot_data['complectation']}\n'''

    is_second_hand = (boot_data['year_of_release'], boot_data['mileage'], boot_data['color'])
    if None not in is_second_hand:
        middle_layer = f'''{LexiconCommodityLoader.load_commodity_year_of_realise['message_text']}: {boot_data['year_of_release']}\
              \n{LexiconCommodityLoader.load_commodity_mileage['message_text']}: {boot_data['mileage']}\
              \n{LexiconCommodityLoader.load_commodity_color['message_text']}: {boot_data['color']}\n'''
        output_load_commodity_config = top_layer + middle_layer + bottom_layer
    else:
        output_load_commodity_config = top_layer + bottom_layer

    return output_load_commodity_config


async def output_load_config_for_seller(request: Union[Message, CallbackQuery], state: FSMContext, photo: dict = None, bot=None):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    create_buttons_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.utils')

    if not bot:
        if isinstance(request, Message):
            # await request.delete()
            bot = request.bot
        else:
            bot = request.message.bot

    if photo:
        await state.update_data(load_photo=photo)

    delete_mode = False

    memory_storage = await state.get_data()
    if memory_storage.get('incorrect_flag'):
        await state.update_data(incorrect_flag=False)
        delete_mode = True

    structured_boot_data = await data_formatter(request=request, state=state)

    output_string = await get_output_string(mode='to_seller',
                                            boot_data=structured_boot_data)

    await message_editor.redis_data.set_data(key=str(request.from_user.id) + ':boot_config', value=output_string)

    output_string = '\n'.join(output_string.split('\n')[:-2])
    output_string += LexiconCommodityLoader.can_rewrite_config
    lexicon_part = await create_buttons_module.create_edit_buttons_for_boot_config(state=state, boot_data=structured_boot_data, output_string=output_string)
    print('lp: ', lexicon_part)
    photo = structured_boot_data['photo_id'] #if not None else structured_boot_data['photo_url']
    # print('photo_id: ', photo)

    await message_editor.redis_data.set_data(key=str(request.from_user.id) + ':can_edit_seller_boot_commodity', value=True)

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part, photo=photo, delete_mode=delete_mode, seller_boot=True, bot=bot)

