import asyncio
import importlib
import logging
import os

import httpx
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

from handlers.custom_filters.message_is_photo import MessageIsPhoto
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from states.load_commodity_states import LoadCommodityStates
# from utils.photo_utils.insert_watermark import insert_watermark

mediagroups = {}
user_messages = []

seller_boot_commodity_module = importlib.import_module(
    'handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs')

async def get_unique_dictionaries(mediagroups):
    unique_mediagroups = {}

    for key, value in mediagroups.items():
        unique_combinations = set()
        unique_dicts = []

        for item in value:
            id_pair = (item.get('id'), item.get('unique_id'))

            if id_pair not in unique_combinations:
                unique_combinations.add(id_pair)
                unique_dicts.append(item)

        unique_mediagroups[key] = unique_dicts

    return unique_mediagroups
async def collect_and_send_mediagroup(message: Message, state: FSMContext, photo_id: int, unique_id: int):

    new_car_state_parameters_module = importlib.import_module(
        'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.new_car_state_parameters_handler')

    '''Обработчик для принятия медиа групп
    Работает с:
    [seller: output_boot_config]'''
    # if message.from_user.is_bot:
    #
    #     return

    try:
        await message.delete()
    except:
        pass
    ic()
    ic(state)

    if not await state.get_state() in (LoadCommodityStates.photo_verification,
                             AdminAdvertParametersStates.NewStateStates.await_input_new_car_photos):

        return
        # pass
    album_id = message.media_group_id
    ic(album_id)
    if album_id:
        if album_id in mediagroups:
            mediagroups[album_id].append({'id': photo_id, 'unique_id': unique_id})
            user_messages.append(message.message_id)
            return
        mediagroups[album_id] = [{'id': photo_id, 'unique_id': unique_id}]
        user_messages.append(message.message_id)
        await asyncio.sleep(2)
        # media_group = await insert_watermark(mediagroups[album_id], message.chat.id, message.bot)

        # new_album = [InputMediaPhoto(media=file_id) for file_id in mediagroups[album_id]]

        # await handle_user_input_photos(album_id, message, state)

        if state:
            state_name = await state.get_state()
            ic(state_name)
            #
            if state_name:
                if state_name in ('LoadCommodityStates:photo_verification', 'AdminAdvertParametersStates.NewStateStates:await_input_new_car_photos'):
                    if not 5 <= len(mediagroups[album_id]) <= 8:

                        photo_filter = MessageIsPhoto()
                        mediagroups.clear()
                        user_messages.clear()
                        await photo_filter(message=message, state=state)
                        return
                    match state_name:
                        case 'LoadCommodityStates:photo_verification':
                            await handle_user_input_photos(album_id, message, state)
                        case 'AdminAdvertParametersStates.NewStateStates:await_input_new_car_photos':
                            await new_car_state_parameters_module\
                                .NewCarStateParameters().callback_handler(message, state, media_photos=mediagroups)
                    mediagroups.clear()

            elif state_name == "MailingStates:uploading_media":
                return mediagroups
    else:
        if state:
            state_name = await state.get_state()
            ic(state_name)
            #
            if state_name:
                match state_name:
                    case 'LoadCommodityStates:photo_verification':
                        await seller_boot_commodity_module.output_load_config_for_seller(request=message, state=state,
                                                                                         media_photos=mediagroups)
                    case 'AdminAdvertParametersStates.NewStateStates:await_input_new_car_photos':
                        await new_car_state_parameters_module\
                            .NewCarStateParameters().callback_handler(message, state, media_photos=mediagroups)


async def handle_user_input_photos(album_id, message, state):
    redis_data_module = importlib.import_module('utils.redis_for_language')
    bot = message.bot
    chat_id = message.chat.id

    async def send_watermark_request(photo_urls):
        url = 'http://localhost:8000/watermark/'
        data = {"photo_list": photo_urls}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                logging.critical(f"Ошибка запроса на добавление вотермарки фотографии: %d\nInputted urls: %s",
                                 str(photo_urls),
                                 response.status_code)



    async def async_remove_photos(file_path):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, os.remove, file_path)



    tasks = [bot.get_file(mediagroup['id']) for mediagroup in mediagroups[album_id]]
    files_info = await asyncio.gather(*tasks)
    urls = [f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}" for file_info in files_info]


    photo_paths = await send_watermark_request(urls)
    ic(photo_paths)
    if photo_paths:
        photo_paths = photo_paths['file_paths']
    else:
        from handlers.utils.message_answer_without_callback import send_message_answer
        Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        await send_message_answer(message, Lexicon_module.ADMIN_LEXICON['unsuccessfully'])
        await seller_boot_commodity_module.output_load_config_for_seller(request=message, state=state,
                                                                         media_photos=[])
        return
    from aiogram.types import FSInputFile
    media_group = [InputMediaPhoto(media=FSInputFile(path)) for path in photo_paths]
    ic(media_group)
    try:
        sendned_media_groups = await bot.send_media_group(chat_id, media=media_group)
        media_photos = [{'id': media_message.photo[-1].file_id, 'unique_id': media_message.photo[-1].file_unique_id} for
                        media_message in sendned_media_groups]

        await redis_data_module.redis_data.set_data(key=f'{chat_id}:last_media_group',
                                                    value=[media_message.message_id
                                                           for media_message in sendned_media_groups])

        await seller_boot_commodity_module.output_load_config_for_seller(request=message, state=state,
                                                                         media_photos=media_photos)
    except:
        #todo
        pass
    finally:
        delete_photos_tasks = [async_remove_photos(file_path) for file_path in photo_paths]
        await asyncio.gather(*delete_photos_tasks)
