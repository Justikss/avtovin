import asyncio
from copy import copy

from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from typing import Union
import importlib

from handlers.utils.create_advert_configuration_block import create_advert_configuration_block
from states.load_commodity_states import LoadCommodityStates
from handlers.state_handlers.seller_states_handler.load_new_car.load_data_fromatter import data_formatter



async def get_output_string(request, mode, boot_data: dict = None, language=None, advert_id=None) -> str:
    '''Метод создаёт строку для вывода выбранных конфигураций загружаемого авто продавцу/админам.'''
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')
    if not language:
        redis_key = f'{str(request.from_user.id)}:language'
        redis_module = importlib.import_module('handlers.default_handlers.start')
        language = await redis_module.redis_data.get_data(key=redis_key)
    if mode:
        if mode == 'to_seller':
            start_sub_string = copy(lexicon_module.commodity_loader_lexicon._data[language]['config_for_seller'])
        elif mode.startswith('to_admins_from_'):
            seller_link = mode.split('_')[3]
            start_sub_string = copy(lexicon_module.commodity_loader_lexicon_ru['config_for_admins']).format(username=seller_link)
    else:
        start_sub_string = ''
    ic(language)
    ic()
    if language != 'ru':
        bottom_layer = f'''\n{boot_data.get('photo_id')}\n{boot_data.get('photo_unique_id')}'''
    else:
        bottom_layer = ''

    top_layer = f'''{start_sub_string}\
{await create_advert_configuration_block(car_state=boot_data['state'], engine_type=boot_data['engine_type'], 
                                         brand=boot_data['brand'], model=boot_data['model'], 
                                         complectation=boot_data['complectation'], color=boot_data['color'], 
                                         mileage=boot_data['mileage'], year_of_realise=boot_data['year_of_release'], 
                                         sum_price= boot_data.get('sum_price'),
                                         usd_price=boot_data.get('dollar_price'), advert_id=advert_id, language=language)}'''

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
    await state.update_data(rewrite_state_flag=None)
    await state.update_data(rewrite_brand_mode=False)
    cars_state = await get_load_car_state_module.get_load_car_state(state=state)

    if cars_state == 'new':
        new_car_photo_requests_module = importlib.import_module('database.data_requests.new_car_photo_requests')
        output_config_module = importlib.import_module(
            'handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs')

        photo_pack = await new_car_photo_requests_module\
            .PhotoRequester.try_get_photo(state)
        ic(photo_pack)
        if photo_pack:
            media_photos=photo_pack
        else:
            if (not memory_storage.get('load_photo') and not media_photos) or need_photo_flag:
                input_photo_module = importlib.import_module(
                    'handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')
                ic(need_photo_flag, memory_storage.get('load_photo'), media_photos)
                ic()

                return await input_photo_module.input_photo_to_load(request, state, need_photo_flag=True)#
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
        ic(media_photos)
        ic()
        await state.update_data(load_photo=media_photos)
        dont_send_media = True
    else:
        dont_send_media = False
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

    # from utils.safe_dict_class import current_language
    redis_key = f'{str(request.from_user.id)}:language'
    redis_module = importlib.import_module('handlers.default_handlers.start')

    output_string = await get_output_string(request, mode='to_seller',
                                            boot_data=structured_boot_data,
                                            language=ic(await redis_module.redis_data.get_data(key=redis_key)
))


    output_string = output_string.replace('None', '').strip()


    lexicon_part = await create_buttons_module.create_edit_buttons_for_boot_config(request, state=state,
                                                                                   boot_data=structured_boot_data,
                                                                                   output_string=output_string)


    await message_editor.redis_data.set_data(key=str(request.from_user.id) + ':can_edit_seller_boot_commodity', value=True)


    await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                    media_group=structured_boot_data.get('photos') if not dont_send_media else None,
                                                    delete_mode=delete_mode or dont_send_media,
                                                    seller_boot=True, bot=bot,
                                                    save_media_group=dont_send_media)


    ic(memory_storage.get('color_for_load'))
    await state.set_state(LoadCommodityStates.load_config_output)