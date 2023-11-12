import asyncio

from aiogram.types import CallbackQuery, Message, InputMediaPhoto
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

mediagroups = {}

async def output_load_config_for_seller(request: Union[Message, CallbackQuery], state: FSMContext, media_photos=None, media_album=None, bot=None):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    create_buttons_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.utils')
    #
    # mediagroups = {}

    # if isinstance(request, Message):
    #     album_id = request.media_group_id
    #     photo_id = request.photo[-1].file_id
    #     print('isis: ', photo_id)
    #     if album_id in mediagroups:
    #         mediagroups[album_id].append(photo_id)
    #         return
    #     mediagroups[album_id] = [photo_id]
    #     await asyncio.sleep(1)
    #
    if media_photos:
        await state.update_data(load_photo=media_photos)



    #     if request.photo:

    #         if album_id in mediagroups:
    #             mediagroups[album_id].append(photo_id)
    #             return
    #
    #         mediagroups[album_id] = [photo_id]
    #         await asyncio.sleep(0.5)
    #         print('mggr: ', mediagroups)



    if not bot:
        if isinstance(request, Message):
            # await request.delete()
            bot = request.bot
        else:
            bot = request.message.bot


    # if isinstance(request, Message):
    #     if request.media_group_id and album[-1].message_id == request.message_id:
    #         photographs = []
    #         print('album ', album)
    #         for message_data in album:
    #             print(message_data)
    #             photographs.append({'file_id': message_data.photo[-1].file_id, 'file_unique_id': message_data.photo[-1].file_unique_id})
    #
    #         await state.update_data(load_photo=photographs)

    delete_mode = False
    memory_storage = await state.get_data()
    #
    # mediagroups_photo = memory_storage.get('load_photo')
    # if mediagroups_photo:
    #     album_id = [key for key, value in mediagroups_photo.items()]
    #     new_album = [InputMediaPhoto(media=file_id) for file_id in mediagroups_photo[album_id]]

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

    await message_editor.redis_data.set_data(key=str(request.from_user.id) + ':can_edit_seller_boot_commodity', value=True)


    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                    media_group=structured_boot_data.get('photos'),
                                                    delete_mode=delete_mode,
                                                    seller_boot=True, bot=bot)

